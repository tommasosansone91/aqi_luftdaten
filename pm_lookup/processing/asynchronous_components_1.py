from concurrent.futures import ThreadPoolExecutor
import asyncio

from pm_lookup.configs.constants import CALLER_CHOICE_BASECOMMAND

from pm_lookup.processing.model_update_triggered_processing_1 import content_of_generate_series_and_draw_graphs


class AsynchronousComponentsToolbox1():
    # this class include all the asynchronous components required to manage the update of the serie parameters model.
    # when it is run by the save method of a model.

    def __init__(self, caller):
        self.caller = caller


    def generate_series_and_draw_graphs(self):

        # Create a thread pool executor.
        # max_workers=1 -> it's set up to manage one thread at a time for executing tasks asynchronously.
        executor_1 = ThreadPoolExecutor(max_workers=1)

        # create a new loop.
        # it manages the execution of asynchronous tasks.

            # Note: You generally want to avoid creating a new event loop and setting it
            # for every call. For simple scripts, it might work, but in a more complex
            # Django application, you might already have an event loop, especially if
            # using ASGI or other async features.

        loop_1 = asyncio.new_event_loop()

        # set the newly created event loop as the current event loop.
        asyncio.set_event_loop(loop_1)

        # Run the async function in the (context of) new event loop, by using the thread pool executor.
        # this offloads the execution of self._run_async to the executor, making it run asynchronously without blocking the main thread.
        future_object_1 = loop_1.run_in_executor(executor_1, self._run_async)

        if self.caller in (CALLER_CHOICE_BASECOMMAND):

            # Wait for the future to complete and get its result (or propagate exceptions).
            # This blocks the main thread (of the management command) until the async task is done.
            loop_1.run_until_complete(future_object_1)

            # Close the loop and shut down the executor cleanly
            loop_1.close()
            executor_1.shutdown(wait=True) # Ensure all tasks are finished before shutting down

            
    def _run_async(self):
        # use asyncio.run() method to run a function that was defined as async.
        # asyncio.run() is used to run coroutines.
        # It handles the event loop management for you, which means it creates a new event loop, runs the coroutine until it completes, and then closes the loop. This is simpler than managing the event loop manually, making it a convenient option for running a single asynchronous function.
        asyncio.run(self.generate_series_and_draw_graphs_async())


    async def generate_series_and_draw_graphs_async(self):
        # when this function is called (without any command before its name), it returns a coroutine

        # execute this coroutine and give me its return value.
        # await is legal only inside an async function.
        await content_of_generate_series_and_draw_graphs()