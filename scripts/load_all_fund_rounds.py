from scripts.fund_round_loaders.load_cof_r2 import main as load_cof_r2
from scripts.fund_round_loaders.load_cof_r3w1 import main as load_cof_r3w1
from scripts.fund_round_loaders.load_cof_r3w2 import main as load_cof_r3w2
from scripts.fund_round_loaders.load_ns_r2 import main as load_ns_r2


def main() -> None:
    load_cof_r2()
    load_cof_r3w1()
    load_cof_r3w2()
    load_ns_r2()


if __name__ == "__main__":
    from app import app

    with app.app_context():
        main()
