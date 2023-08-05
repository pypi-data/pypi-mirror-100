"""
Scripts de console
"""
from kt_otm import kt_otm
from kt_otm import __version__
import click


@click.command()
@click.argument("preco", type=float, required=False)
@click.option("--version", is_flag=True, help="Exibe a versao")
def cli(preco, version):
    """Calcula strikes fora do dinheiro."""
    if version:
        click.echo("kt-otm %s" % __version__)
        return 0
    if not preco:
        click.echo("Usage: otm [OPTIONS] [PRECO]")
        return 0
    preco = float(preco)
    call_otm = kt_otm.call(preco)
    put_otm = kt_otm.put(preco)
    click.echo("%.2f" % call_otm)
    click.echo("%.2f" % put_otm)
