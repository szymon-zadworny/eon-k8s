from argparse import ArgumentParser
from pathlib import Path
from shutil import rmtree
from jinja2 import Environment, PackageLoader, select_autoescape


def main():
    args = get_args()
    try:
        save_dir = create_save_dir('scenario')
    except Exception as e:
        print(e)
        print("Aborting...")
        return

    for (filename, content) in get_object_publish_scenario_yaml(args.step, args.nodes):
        path = save_dir / filename
        path.write_text(content)

    
def get_object_publish_scenario_yaml(step, nodes):
    env = Environment(
        loader=PackageLoader("generate"),
        autoescape=select_autoescape()
    )

    generated_files = []

    bootstrap = env.get_template("bootstrap-service.yaml")
    filename = "bootstrap-service.yaml"
    generated_files.append(filename)
    yield (filename, bootstrap.render())

    node = env.get_template("node-job.yaml")
    
    # Nodes other than bootstrap, provider and consumer
    for n in range(nodes - 3):
        job = node.render(delay=f"{(n + 1) * step} ms")
        filename = f"node-job-{n}.yaml"
        generated_files.append(filename)
        yield (filename, job)

    provider = env.get_template("provider-job.yaml")
    filename = "provider-job.yaml"
    generated_files.append(filename)
    yield (filename, provider.render(delay=f"{(nodes - 2) * step} ms"))
        
    consumer = env.get_template("consumer-job.yaml")
    filename = "consumer-job.yaml"
    generated_files.append(filename)
    yield (filename, consumer.render(delay=f"{(nodes - 1) * step} ms"))

    kustomization = env.get_template("kustomization.yaml")
    yield ("kustomization.yaml", kustomization.render(files=generated_files))


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
