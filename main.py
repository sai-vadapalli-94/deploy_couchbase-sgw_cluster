# documentation link: https://docs.couchbase.com/server/current/install/getting-started-docker.html
from fmodule import *

def main():
    """
    This function prompts the user for a version of Couchbase, then performs a series of
    operations to manage Docker containers and images related to Couchbase.

    The operations performed by this function are:
    - Prompt the user for a version of Couchbase to pull
    - Check Docker version
    - List Docker containers
    - Remove exited containers
    - Pull Docker image for specified version of Couchbase
    - List Docker images for specified version of Couchbase
    - Run Docker containers for specified version of Couchbase
    - Display IP address of Docker containers in case if someone whats to access the shell of the containers
    - Configure the Couchbase initial node
    - Initialize the Couchbase nodes
    - Perform rebalance operation for added nodes
    - Pull Docker image for SGW (CB Sync Gateway)
    """

    # Prompt the user for a version of Couchbase to pull
    version: str = input("\nEnter the version of couchbase you want to pull: ")
    print("\n")
    # Check Docker version
    check_docker_version()

    # List Docker containers
    list_containers()

    # Stop Docker containers
    stop_containers()

    # Remove exited containers
    remove_exited_containers()

    # Pull Docker image for specified version of Couchbase
    pull_docker_image(version)

    # List Docker images for specified version of Couchbase
    list_docker_images(version)

    # Run Docker containers for specified version of Couchbase
    run_containers(version)

    # Display IP address of Docker containers
    display_container_ip("default")

    # Configure the Couchbase init node
    configure_init_node()

    # Initialize the Couchbase nodes
    nodes_init()

    # Perform rebalance operation
    perform_rebalance()

    # Pull Docker image for SGW (Search Gateway)
    sgw_pull_image()
    
    # user creation
    create_cb_user_for_sgw()

    # Configure SGW
    configure_sgw()


if __name__ == "__main__":
    main()
