class PortfolioMiddleware(object):
    def process_request(self, request):
        print "Middleware executed"