import utils

def Inicialize_fw():
    # Crear una tabla inet llamada 'filter'
    utils.run_nft_command(["add", "table", utils.gen_family, "filter"])

    # Crear la cadena 'input' con política 'drop' por defecto
    utils.run_nft_command(["add", "chain", utils.gen_family, "filter", "input",
                     "{", "type", "filter", "hook", "input", "priority", "0;", "policy", "drop;", "}"])

    # Crear la cadena 'forward' con política 'drop' por defecto
    utils.run_nft_command(["add", "chain", utils.gen_family, "filter", "forward",
                     "{", "type", "filter", "hook", "forward", "priority", "0;", "policy", "drop;", "}"])

    # Crear la cadena 'output' con política 'accept' por defecto
    utils.run_nft_command(["add", "chain", utils.gen_family, "filter", "output",
                     "{", "type", "filter", "hook", "output", "priority", "0;", "policy", "accept;", "}"])

    # Permitir tráfico de loopback (localhost)
    utils.run_nft_command(["add", "rule", utils.gen_family, "filter", "input", "iif", "lo", "accept"])

    # Permitir tráfico ICMP (ping)
    utils.run_nft_command(["add", "rule", utils.gen_family, "filter", "input", "ip", "protocol", "icmp", "accept"])

    # Permitir tráfico en puertos comunes (SSH, HTTP, HTTPS)
    utils.run_nft_command(["add", "rule", utils.gen_family, "filter", "input", "tcp", "dport", "22", "accept"])  # SSH
    utils.run_nft_command(["add", "rule", utils.gen_family, "filter", "input", "tcp", "dport", "80", "accept"])  # HTTP
    utils.run_nft_command(["add", "rule", utils.gen_family, "filter", "input", "tcp", "dport", "443", "accept"])  # HTTPS

    # Permitir tráfico relacionado y establecido (conexiones de retorno)
    utils.run_nft_command(["add", "rule", utils.gen_family, "filter", "input", "ct", "state",
                     "related,established", "accept"])

    # Bloquear todo lo demas
    utils.run_nft_command(["add", "rule", utils.gen_family, "filter", "input", "counter", "drop"])

def copy_ruleset(file_path):
    return utils.copy_stdout_nft_command(["list","ruleset"],file_path)

def list_ruleset():

    command = ["-a","list", "ruleset"]
    return utils.run_nft_command(command)

def add_table(name):
    command= ["add","table",utils.gen_family, name]
    return utils.run_nft_command(command)

def list_tables():
    command= ["list","tables"]
    return utils.run_nft_command(command)

def delete_table(name):
    command= ["delete","table",utils.gen_family, name]
    return utils.run_nft_command(command)

def delete_table(name):
    command = ["delete", "table", utils.gen_family, name]
    return utils.run_nft_command(command)

def flush_table(name):
    """En algun kernel de linux previo a la version 3.28 puede requerir
     flushear la tabla primero( es decir vaciar su contenido)"""
    command = ["flush", "table", utils.gen_family, name]
    return utils.run_nft_command(command)

def add_chain(table,name, type, hook, priority, policy=None, comment=None):
    command = [ "add", "chain", utils.gen_family, table, name, "{ type", type, "hook", hook, "priority", priority, ";"]
    if (policy or comment):

      if policy:
          command += ["policy", policy, ";"]
      if comment:
          command += ["comment", '\"', comment, '\";']

    command += ["}"]
    return utils.run_nft_command(command)

def delete_chain(table, name):
    command=["delete", "chain", utils.gen_family, table, name]
    return utils.run_nft_command(command)

def add_rule(table, chain, rule):
    """En este caso se ha ignorado el parametro de <family> de las reglas de nftables, suponienod quye va a ser siempre
    en futuraas configuraciones se puede modificar para que este parametro sea modificable"""

    """
    AÑADIR:
    algun tipo de gestion de error en caso de que la tabla que se llama o chain no exista, pata que se pueda corregir
    """
    command = ["add", "rule", utils.gen_family, table, chain] + rule.split()
    return utils.run_nft_command(command)

def list_rules_from_tables(name):
    command = ["-a","list", "table", utils.gen_family, name]
    return utils.run_nft_command(command)

def delete_rule(table, chain, handler):
    """En este caso se ha ignorado el parametro de <family> de las reglas de nftables, suponienod quye va a ser siempre
        en futuraas configuraciones se puede modificar para que este parametro sea modificable"""

    command = ["delete", "rule", utils.gen_family, table, chain, "handle", handler]
    return utils.run_nft_command(command)


if __name__ == "__main__":
  Inicialize_fw()