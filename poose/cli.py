import argparse
def main(argv: list[str] | None = None ):
    p = argparse.ArgumentParser(
        prog="poose",
        description="migration tool for sqlite"
    )

    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("create").add_argument("name")

    up = sub.add_parser("up")
    up.add_argument("--to", default=None)

    down = sub.add_parser("down")
    down.add_argument("-n","--step", type=int, default=1)

    reset = sub.add_parser("reset")
    redo = sub.add_parser("redo")
    status = sub.add_parser("status")
    version = sub.add_parser("version")

    args = p.parse_args(argv)
    match args.cmd:
        case "status":
            print("status")
        case "up":
            print("up")
        case "down":
            print("down")
        case "version":
            print("version")
        case "reset":
            print("rest")
        case "create":
            print(f"create {args.name}")

    return 0
        

if __name__ == "__main__":
   main() 

    