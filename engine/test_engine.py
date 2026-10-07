from engine.order_book import OrderBook


def test_order_book():

    book = OrderBook()

    book.add_order(
        b"B",
        100.0,
        10
    )

    book.add_order(
        b"S",
        99.0,
        10
    )

    assert book.get_trade_count() == 10

    print("Engine test passed.")


if __name__ == "__main__":
    test_order_book()