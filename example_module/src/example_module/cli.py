import click
import example_module


@click.command()
def test():
    print('NAME saved as', example_module.config['NAME'])
    print('DATA_DIR located at', example_module.config['DATA_DIR'])
    print('SOME_NUMBER saved as', example_module.config['SOME_NUMBER'])


@click.command()
@click.argument('group')
@click.option('--reset/--no-reset', default=False, help='Delete existing group keys in config')
def configure(group, reset):
    example_module.config.update(group, reset)


@click.group()
def main():
    pass

main.add_command(test)
main.add_command(configure)

if __name__ == '__main__':
    main()