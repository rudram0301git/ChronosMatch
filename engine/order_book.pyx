"""
Simple Cython order book for ChronosMatch.
"""

cdef class OrderBook:

    cdef list buy_orders
    cdef list sell_orders
    cdef int trade_count

    def __cinit__(self):
        self.buy_orders = []
        self.sell_orders = []
        self.trade_count = 0

    def add_order(
        self,
        side,
        double price,
        int quantity
    ):

        if side == b"B":
            self.buy_orders.append(
                (price, quantity)
            )

        elif side == b"S":
            self.sell_orders.append(
                (price, quantity)
            )

        self.match_orders()

    cdef match_orders(self):

        while (
            len(self.buy_orders) > 0
            and len(self.sell_orders) > 0
        ):

            buy_price = self.buy_orders[0][0]
            sell_price = self.sell_orders[0][0]

            if buy_price >= sell_price:

                buy_quantity = self.buy_orders[0][1]
                sell_quantity = self.sell_orders[0][1]

                trade_quantity = min(
                    buy_quantity,
                    sell_quantity
                )

                self.trade_count += trade_quantity

                if buy_quantity > trade_quantity:
                    self.buy_orders[0] = (
                        buy_price,
                        buy_quantity - trade_quantity
                    )
                else:
                    self.buy_orders.pop(0)

                if sell_quantity > trade_quantity:
                    self.sell_orders[0] = (
                        sell_price,
                        sell_quantity - trade_quantity
                    )
                else:
                    self.sell_orders.pop(0)

            else:
                break

    def get_trade_count(self):
        return self.trade_count