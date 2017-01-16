from ctypes import c_char_p
import logging
import traceback
from multiprocessing import Semaphore, Condition, Lock, Value, Pipe, Process


class Task:

    class State:

        def __init__(self):
            pass

        NEW = 'NEW'
        RUNNING = 'RUNNING'
        DONE = 'DONE'
        FAILED = 'FAILED'

    def parse_state(self, string):
        if string == Task.State.NEW:
            return Task.State.NEW
        elif string == Task.State.RUNNING:
            return Task.State.RUNNING
        elif string == Task.State.DONE:
            return Task.State.DONE
        elif string == Task.State.FAILED:
            return Task.State.FAILED
        else:
            raise AttributeError('Invalid state: %s', string)

    def __init__(self, name):
        self.name = name
        self.dependencies = set()
        self.state = Task.State.NEW
        self.result_proxy = None

    def __str__(self):
        return self.name

    def update(self):
        if self.result_proxy is not None and self.result_proxy.value is not '':
            logging.debug("Updating task %s to status %s", self.name, self.result_proxy.value)
            self.state = self.parse_state(self.result_proxy.value)
            self.result_proxy = None #reset to None to avoid 'RuntimeError: Synchronized objects should only be shared between processes through inheritance'

    def has_resolved_dependencies(self):
        """Return True if all dependencies are in State.DONE"""
        for dependency in self.dependencies:
            if dependency.state != Task.State.DONE:
                return False

        return True

    def is_new(self):
        return self.state == Task.State.NEW

    def dependencies_as_list(self):
        """Returns a list of dependency names."""
        dependencies = []
        for dependency in self.dependencies:
            dependencies.append(dependency.name)
        return dependencies

    def dependencies_as_string(self):
        """Returns a comma separated list of dependency names."""
        return ",".join(self.dependencies_as_list())

    def ordered_dependencies(self):
        ordered_dependencies = self._all_dependencies()
        return ordered_dependencies

    def _all_dependencies(self):
        deps = []
        unprocessed_deps = [self]
        processed_deps = []
        while unprocessed_deps:
            dep = unprocessed_deps.pop()
            if dep.dependencies and dep not in processed_deps and \
               not set(dep.dependencies).issubset(set(processed_deps)):
                unprocessed_deps += [dep] + list(dep.dependencies)
                processed_deps.append(dep)
            elif dep not in deps and dep is not self:
                deps.append(dep)

        return deps

    def has_dependencies(self):
        return len(self.dependencies) > 0


class Tasks:

    def __init__(self):
        self.tasks = {}
        self.dirty = True

    def get_task(self, name):
        """Get task by name or create it if it does not exists."""
        if name in self.tasks.keys():
            task = self.tasks[name]
        else:
            task = Task(name)
            self.tasks[name] = task
        return task

    def add(self, task_name, dependency_names=set()):
        task = self.get_task(task_name)
        for dependency_name in dependency_names:
            dependency = self.get_task(dependency_name)
            task.dependencies.add(dependency)

        self.dirty = True

    def get_next(self):
        """Return next task from the stack that has all dependencies resolved.
        Return None if there are no tasks with resolved dependencies or is there are no more tasks on stack.
        Use `count` to check is there are still some task left on the stack.

        raise ValueError if total ordering is not possible."""

        self.update_tasks_status()

        if self.dirty:
            self.tsort()
            self.dirty = False

        for key, task in self.tasks.iteritems():
            if task.is_new() and task.has_resolved_dependencies():
                return task

        return None

    def count(self, state):
        self.update_tasks_status()
        count = 0
        for key, task in self.tasks.iteritems():
            if task.state == state:
                count += 1
        return count

    def print_name(self, state):
        list = ""
        for key, task in self.tasks.iteritems():
            if task.state == state:
                if list != "":
                    list += " "+task.name
                else:
                    list = task.name
        return list
                 

    def update_tasks_status(self):
        for key, task in self.tasks.iteritems():
            task.update()

    def are_dependencies_buildable(self, task):
        for dependency in task.dependencies:
            if dependency.state is Task.State.FAILED:
                return False
            else:
                if not self.are_dependencies_buildable(dependency):
                    return False
        return True

    def count_buildable_tasks(self):
        """Count tasks that are new and have dependencies in non FAILED state."""
        self.update_tasks_status()
        buildable_tasks_count = 0
        for key, task in self.tasks.iteritems():
            if task.state is Task.State.NEW:
                if self.are_dependencies_buildable(task):
                    buildable_tasks_count += 1
                    logging.debug("Buildable task: %s" % task.name )
                else:
                    logging.debug("Task %s has broken dependencies." % task.name )

        return buildable_tasks_count

    def filter_tasks(self, task_names, keep_dependencies=False):
        """If filter is applied only tasks with given name and its dependencies (if keep_keep_dependencies=True) are kept in the list of tasks."""
        new_tasks = {}
        for task_name in task_names:
            task = self.get_task(task_name)
            if task not in new_tasks:
                new_tasks[task.name] = task
            if keep_dependencies:
                for dependency in task.ordered_dependencies():
                    if dependency not in new_tasks:
                        new_tasks[dependency.name] = dependency
            else:
                #strip dependencies
                task.dependencies = set()

        self.tasks = new_tasks

    #todo private
    def tsort(self):
        """Given a partial ordering, return a totally ordered list.

        part is a dict of partial orderings.  Each value is a set,
        which the key depends on.

        The return value is a list of sets, each of which has only
        dependencies on items in previous entries in the list.

        raise ValueError if ordering is not possible (check for circular or missing dependencies)"""

        task_dict = {}
        for key, task in self.tasks.iteritems():
            task_dict[task] = task.dependencies
        # parts = parts.copy()
        parts = task_dict.copy()

        result = []
        while True:
            level = set([name for name, deps in parts.iteritems() if not deps])
            if not level:
                break
            result.append(level)
            parts = dict([(name, deps - level) for name, deps in parts.iteritems() if name not in level])
        if parts:
            raise ValueError, 'total ordering not possible (check for circular or missing dependencies)'
        return result

    def get_all(self):
        return self.tasks


class TaskRunner:
    """TaskRunner is used for parallel execution of tasks (replacement for make)"""

    def __init__(self, run_build):
        self.run_build = run_build

    def wait_tasks_to_complete(self, parallel_threads, process_finished_notify, semaphore):
        logging.debug("Checking if there are running tasks.")
        if semaphore.get_value() < parallel_threads: #is any task running
            process_finished_notify.acquire()
            logging.debug("Waiting for tasks to complete.")
            process_finished_notify.wait()
            logging.debug("Finished waiting tasks to complete.")
            process_finished_notify.release()

    def run(self, tasks, build_config, parallel_threads):
        semaphore = Semaphore(parallel_threads)
        process_finished_notify = Condition(Lock())
        while tasks.count_buildable_tasks() > 0:
            task = tasks.get_next()

            if task is None:
                self.wait_tasks_to_complete(parallel_threads, process_finished_notify, semaphore)
                continue

            semaphore.acquire()
            task.state = Task.State.RUNNING
            logging.debug("Starting task %s", task.name)
            self.start_new_process(process_finished_notify, semaphore, self.process_job, task, build_config)

        self.wait_tasks_to_complete(parallel_threads, process_finished_notify, semaphore)

        if tasks.count(Task.State.FAILED) > 0:
            logging.error('Some packages failed to build.')
            logging.error("  %s", tasks.print_name(Task.State.FAILED))
            return 1
        if tasks.count(Task.State.RUNNING) > 0:
            logging.error('Something went wrong, there are still some running tasks.')
            return 1
        if tasks.count(Task.State.NEW) > 0:
            logging.error('Something went wrong, there are still unprocessed tasks.')
            return 1

        logging.info("Build completed successfully.")
        return 0

    def start_new_process(self, process_finished_notify, semaphore, target_method, task, build_config):
        result_val = Value(c_char_p, '')
        task_conn, task_conn_remote = Pipe()
        config_conn, config_conn_remote = Pipe()
        p = Process(target=target_method, args=[semaphore, process_finished_notify, task_conn_remote, config_conn_remote, result_val])
        p.daemon = True
        logging.debug("Sending task: %s", task.name)
        task_conn.send(task)
        config_conn.send(build_config)
        task.result_proxy = result_val
        p.start()

    def process_job(self, semaphore, process_finished_notify, task_conn, config_conn, result_proxy):
        task = task_conn.recv()
        build_config = config_conn.recv()

        try:
            exit_status = self.run_build(task, build_config)
        except Exception:
            print traceback.format_exc()
            exit_status = 1

        if exit_status != 0:
            result_proxy.value = Task.State.FAILED
        else:
            result_proxy.value = Task.State.DONE

        process_finished_notify.acquire()
        semaphore.release()
        process_finished_notify.notify()
        process_finished_notify.release()
        logging.debug("Task %s finished.", task.name)
