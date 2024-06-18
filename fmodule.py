# documentation link: https://docs.couchbase.com/server/current/install/getting-started-docker.html
import os
import subprocess

# TODO: make a persistent volume -> Pending
# TODO: load sample buckets from a sample db user
# TODO: add exception handling in case of errors for all the functions -> pending
# TODO: print a summary of all the details of the cluster like login, the hostname of cluster to access webui

# global variables for credentials
username = "Administrator"
password = "admin123"

def check_docker_version() -> None:
    """
    Check the Docker version on the server and client by running 'docker version'.
    This function does not take any parameters and does not return anything.
    """

    print("****************************** Checking connectivity between the server and client:******************************")
    os.system("docker version")
    print("\n")


def list_containers() -> None:
    """
    A function that lists all containers by executing 'docker ps -a' command.
    
    This function does not take any parameters and does not return anything.
    """

    print("listing all containers: ")
    list_cmd = f"docker ps -a"
    os.system(list_cmd)

def stop_containers() -> None:
    """
    Stops the containers named cbn1, cbn2, and cbn3. 
    Uses `docker container stop` to stop the containers. 
    """

    print("\n")
    print("\n****************************** Stopping all couchbase containers deployed by the script[cbn1, cbn2, cbn3] ******************************")
    stop_cmd = f"docker container stop cbn1 cbn2 cbn3"
    os.system(stop_cmd)

def remove_exited_containers() -> None:
    """
    Uses `docker container rm` to remove all exited containers.
    This function does not take any parameters and does not return anything.

    """

    print(f"****************************** Removing all the exited containers ******************************\n")
    remove_cmd = f"docker container rm -f cbn1 cbn2 cbn3"
    os.system(remove_cmd)
    print("\n")

def pull_docker_image(version: str) -> None:
    """
    Pulls the Couchbase Docker image with the specified version.

    Args:
        version (str): The version of the Couchbase Docker image to pull.

    Returns:
        None: This function does not return anything.

    This function prints a message indicating that it is pulling the Couchbase Docker image with the specified version.
    It then constructs the Docker pull command using the provided version and executes it using the `os.system` function.
    """

    print("****************************** Pulling the couchbase image ******************************\n")
    image_pull = f"docker pull couchbase:enterprise-{version}"
    os.system(image_pull)


def list_docker_images(version: str) -> None:
    """
    Lists all the Docker images of the specified Couchbase version.

    Args:
        version (str): The version of the Couchbase image to list.

    Returns:
        None
    """

    print("****************************** Listing all images of couchbase ******************************")
    list_images = f"docker images couchbase:enterprise-{version}"
    os.system(list_images)


def run_containers(version: str) -> None:
    """
    Runs three Couchbase containers with the specified version.

    Args:
        version (str): The version of Couchbase to run.

    Returns:
        None: This function does not return anything.

    This function runs three Couchbase containers with the specified version. It prints a message indicating the start of the containers and then runs the containers using the `docker run` command. The containers are named `cbn1`, `cbn2`, and `cbn3` respectively. The containers are mapped to ports `8091-8096` and `11210-11211`. The output of the `docker run` command is captured and printed.

    Note:
        This function uses the `subprocess.run` function to run the `docker run` command. The `shell=True` argument is used to run the command in a shell. The `capture_output=True` argument captures the output of the command.

    Example:
        >>> module.run_containers("7.0.3")
        ****************************** Running the couchbase containers ******************************

        Container cbn1: <output of docker container id for cbn1>
    """
    # remove code smell later
    print("\n")
    print("****************************** Running the couchbase containers ******************************")
    init_container = f"cbn1"
    # docker run -d --name cbn3 -p 8091-8096:8091-8096 -p 11210-11211:11210-11211 couchbase
    run_cmd_init = f"docker run -d --name {init_container} -p 8091-8096:8091-8096 -p 11210-11211:11210-11211 couchbase:{version}"
    container_cbn1 = subprocess.run(run_cmd_init, shell=True, capture_output=True, text=True)
    print(f"Container cbn1: {container_cbn1.stdout.strip()}")
    
    second_container = f"cbn2"
    run_cmd_second = f"docker run -d --name {second_container} couchbase:{version}"
    container_cbn2 = subprocess.run(run_cmd_second, shell=True, capture_output=True, text=True)
    print(f"Container cbn2: {container_cbn2.stdout.strip()}")

    third_container = f"cbn3"
    run_cmd_third = f"docker run -d --name {third_container}  couchbase:{version}"
    container_cbn3 = subprocess.run(run_cmd_third, shell=True, capture_output=True, text=True)
    print(f"Container cbn3: {container_cbn3.stdout.strip()}")
    print("\n")


def display_container_ip() -> None:
    """
    Display the IP addresses of the containers cbn1, cbn2, and cbn3.

    This function executes the `docker inspect` command to retrieve the IP addresses of the containers.
    It then prints the IP addresses of each container.

    Parameters:
        None

    Returns:
        None
    """

    print("\n")
    print("****************************** Displaying container ip addresses ****************************** ")
    # docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' cbn1
    
    first_container_ip  = "docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' cbn1"
    second_container_ip = "docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' cbn2"
    third_container_ip  = "docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' cbn3"
    
    cbn1_ip = subprocess.run(first_container_ip, shell=True, capture_output=True, text=True)
    cbn2_ip = subprocess.run(second_container_ip, shell=True, capture_output=True, text=True)
    cbn3_ip = subprocess.run(third_container_ip, shell=True, capture_output=True, text=True)
    
    strip_cbn1_ip = cbn1_ip.stdout.strip()
    strip_cbn2_ip = cbn2_ip.stdout.strip()
    strip_cbn3_ip = cbn3_ip.stdout.strip()
    
    print(f"cbn1 ip: {strip_cbn1_ip}")
    print(f"cbn2 ip: {strip_cbn2_ip}")
    print(f"cbn3 ip: {strip_cbn3_ip}")


def configure_init_node() -> None:
    """
    Configures the initial node by setting up the cluster with specific RAM sizes and services.
    This function initializes the Couchbase cluster by executing the necessary commands using the provided container IP address,
    username, and password. It also prints the username and password used for the cluster setup.
    """

    print("****************************** Configuring the nodes ******************************")
    # TODO: remove the code smell later

    command0 = "docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' cbn1"
    result = subprocess.run(command0, shell=True, capture_output=True, text=True)
    container_ip_addr = result.stdout.strip()

    os.system("sleep 10")

    data_ramsize = "2048"
    index_ramsize = "512"
    eventing_ramsize = "512"
    fts_ramsize = "512"
    analytics_ramsize = "1024"

    cluster_init = f"""/opt/couchbase/bin/couchbase-cli cluster-init -c {container_ip_addr} --cluster-name cb-test --cluster-username {username} \
    --cluster-password {password} --services data,index,query,fts,analytics \
    --cluster-ramsize {data_ramsize} --cluster-index-ramsize {index_ramsize} \
    --cluster-eventing-ramsize  {eventing_ramsize} --cluster-fts-ramsize {fts_ramsize} \
    --cluster-analytics-ramsize  {analytics_ramsize} --cluster-fts-ramsize {fts_ramsize} \
    --index-storage-setting default
    """
    run_cmd = f'docker exec cbn1 /bin/bash -c "{cluster_init}"'
    os.system(run_cmd)
    print(f"The username is: {username}")
    print(f"The password is: {password}")
    print("\n")

def nodes_init() -> None:
    """
    Initializes the nodes in the Couchbase cluster by adding the IP addresses of the containers cbn1, cbn2, and cbn3 to the cluster.
    The IP addresses of the containers are retrieved using the `docker inspect` command. The `couchbase-cli server-add` command is executed
    to add the IP addresses to the cluster. The `--username` and `--password` parameters are set to the provided username and password.
    The `--services` parameter specifies the services to be enabled for each container. The function waits for 5 seconds and then executes
    the `couchbase-cli server-add` command for each container using the `docker exec` command. The function waits for 15 seconds between
    executing the commands for each container.

    Parameters:
        None

    Returns:
        None
    """
    print("****************************** Adding nodes to the cluster ******************************")
    
    first_container_ip  = "docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' cbn1"
    second_container_ip = "docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' cbn2"
    third_container_ip  = "docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' cbn3"

    cbn1_ip = subprocess.run(first_container_ip, shell=True, capture_output=True, text=True)
    cbn2_ip = subprocess.run(second_container_ip, shell=True, capture_output=True, text=True)
    cbn3_ip = subprocess.run(third_container_ip, shell=True, capture_output=True, text=True)
    
    strip_cbn1_ip = cbn1_ip.stdout.strip()
    strip_cbn2_ip = cbn2_ip.stdout.strip()
    strip_cbn3_ip = cbn3_ip.stdout.strip()

    server_init1 = f"""
    couchbase-cli server-add -c {strip_cbn1_ip} --username {username} \
    --password {password} --server-add {strip_cbn2_ip} \
    --server-add-username {username} --server-add-password {password} \
    --services data,index,query,analytics,eventing 
    """

    server_init2 = f"""
    couchbase-cli server-add -c {strip_cbn1_ip} --username {username} \
    --password {password} --server-add {strip_cbn3_ip} \
    --server-add-username {username} --server-add-password {password} \
    --services data,index,query,analytics,eventing 
    """

    sleep  = "sleep 5"
    os.system(sleep)

    exec_cmd_cbn2 = f'docker exec cbn2 /bin/bash -c "{server_init1}"'
    exec_cmd_cbn3 = f'docker exec cbn3 /bin/bash -c "{server_init2}"'

    os.system(exec_cmd_cbn2)
    sleep  = "sleep 15"
    os.system(sleep)
    os.system(exec_cmd_cbn3)
    

def perform_rebalance() -> None:
    """
    Perform a rebalance operation on the Couchbase cluster.

    This function prints a message indicating that the rebalance operation is being performed.
    It then constructs the command to rebalance the cluster using the `couchbase-cli` tool.
    The command is executed using the `docker exec` command on the `cbn1` container.
    After the rebalance operation, the function waits for 15 seconds using the `sleep` command.
    Finally, it prints a message indicating that the rebalance operation has completed.

    This function does not take any parameters and does not return anything.
    """

    print("\n")
    print("****************************** Performing to rebalance the cluster ******************************")
    cb_cli_rebalance = f"/opt/couchbase/bin/couchbase-cli rebalance -c localhost -u {username} -p {password} --no-progress-bar --no-wait"
    rebalance_cbcli = f"docker exec cbn1 /bin/bash -c '{cb_cli_rebalance}'"
    os.system(rebalance_cbcli)
    os.system("sleep 15")
    print("\n")

def pause_containers() -> None:
    """
    Pauses all Couchbase containers deployed by the script [cbn1, cbn2, cbn3].

    This function prints a message indicating that all Couchbase containers are being paused.
    It constructs the command to pause the containers using the `docker pause` command.
    The command is executed using the `os.system` function.

    Parameters:
        None

    Returns:
        None
    """
    print("****************************** Pausing all couchbase containers deployed by the script[cbn1, cbn2, cbn3] ******************************")
    pause_cmd = f"docker pause cbn1 cbn2 cbn3"
    os.system(pause_cmd)

# have this here to invoke this using the python repl after importing the module
def unpause_containers() -> None:
    """
    Unpauses all Couchbase containers deployed by the script [cbn1, cbn2, cbn3].

    This function prints a message indicating that all Couchbase containers are being unpaused.
    It constructs the command to unpause the containers using the `docker unpause` command.
    The command is executed using the `os.system` function.

    Parameters:
        None

    Returns:
        None
    """
    print("****************************** Unpausing all couchbase containers deployed by the script[cbn1, cbn2, cbn3] ******************************")
    unpause_cmd = f"docker unpause cbn1 cbn2 cbn3"
    os.system(unpause_cmd)

def start_containers() -> None:
    """
    Starts all Couchbase containers deployed by the script [cbn1, cbn2, cbn3].

    This function prints a message indicating that all Couchbase containers are being started.
    It constructs the command to start the containers using the `docker start` command.
    The command is executed using the `os.system` function.

    Parameters:
        None

    Returns:
        None
    """
    print("****************************** Starting all couchbase containers deployed by the script[cbn1, cbn2, cbn3] ******************************")
    start_cmd = f"docker start cbn1 cbn2 cbn3"
    os.system(start_cmd)

def sgw_pull_image() -> None:
    """
    Pulls the sync gateway image from the Docker registry.

    This function prints a message indicating that the sync gateway image is being pulled.
    It constructs the command to pull the image using the `docker pull` command.
    The command is executed using the `os.system` function.

    This function does not take any parameters and does not return anything.
    """

    print("****************************** Pulling the sync gateway image ******************************\n")
    image_pull = f"docker pull couchbase/syncgateway"
    os.system(image_pull)


def configure_sgw() -> None:
    ...