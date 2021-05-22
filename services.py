import eventlet, time
from nameko.web.handlers import http


class Service:
    name = "Service"

    @http("GET", "/")
    def nameko_graphql_web_lives_here(self, request):
        return "Nameko graphql-web lives here."

    @http("GET", "/simple")
    def simple(self, request):
        return "Nameko says 'hi'."

    @http("GET", "/sleep/<int:nap>")
    def sleep(self, request, nap):
        # is_patched = eventlet.patcher.is_monkey_patched(time)
        # slept = 0
        # for loops in range(nap):
        #     eventlet.greenthread.sleep(0.10)
        #     time.sleep(1)
        #     slept += 1
        # return f"Nameko slept {nap} {'patched ' if is_patched else 'unpatched '}seconds with every second, 0.10 seconds of cooperative greentime."
        eventlet.sleep(nap)
        return "slept"
