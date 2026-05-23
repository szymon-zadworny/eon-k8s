from argparse import ArgumentParser


def main():
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
    args = parser.parse_args()
    print(args)


if __name__ == "__main__":
    main()
