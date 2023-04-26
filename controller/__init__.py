from .address_book.address_book import router as address_book_router
class Routes:
    def __init__(self,app):
        self.app = app
    def include_routers(self):
        self.app.include_router(address_book_router, prefix="/api/address", tags=["address"])