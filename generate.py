from argparse import ArgumentParser
from pathlib import Path
from shutil import rmtree


def main():
    args = get_args()
    try:
        save_dir = create_save_dir('scenario')
    except Exception as e:
        print(e)
        print("Aborting...")
        return


def get_args():
    parser = ArgumentParser(
        prog='eon-k8s-generate',
        description='A generator for Kubernetes-based EON simulation scenarios'
    )
    parser.add_argument('-s', '--step',
                        help='Time (ms) each simulation step takes',
                        default=300)
    parser.add_argument('-n', '--nodes',
                        help='Number of simulated nodes',
                        default=20)
    return parser.parse_args()


def create_save_dir(name):
    save_dir = Path(name)

    while True:
        try:
            save_dir.mkdir()
        except FileExistsError:
            ans = input(f"{name} exists. Overwrite? [y/n]: ")

            if ans == 'n':
                raise

            if save_dir.is_dir():
                rmtree(save_dir)
            else:
                save_dir.unlink()

            continue
        except Exception as e:
            raise
        else:
            return save_dir


if __name__ == "__main__":
    main()
