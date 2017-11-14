# This helps me to share my SSH keys to the docker container
# I'm using to build stuff. This is needed if you need to
# pull stuff from private repos, for example.

# To build the image, run ...
# docker build -t swift:ssh --build-arg ssh_prv_key="$(cat ~/.ssh/id_rsa)" --build-arg ssh_pub_key="$(cat ~/.ssh/id_rsa.pub)" . -f Swift.Dockerfile
#
# Then, quickly run a container ...
# docker run -it --rm --name swift-temp swift:temp /bin/bash
#
# In the shell, run ...
# eval "$(ssh-agent)" && ssh-add ~/.ssh/id_rsa
#
# Finally, open another shell and run ...
# docker commit swift-temp swift:ssh

FROM swift:latest

ARG ssh_prv_key
ARG ssh_pub_key

RUN apt-get update && \
    apt-get install -y \
        git \
        openssh-server

# Authorize SSH Host
RUN mkdir -p /root/.ssh && \
    chmod 0700 /root/.ssh && \
    ssh-keyscan github.com > /root/.ssh/known_hosts && \
    ssh-keyscan gitlab.com > /root/.ssh/known_hosts

# Add the keys and set permissions
RUN echo "$ssh_prv_key" > /root/.ssh/id_rsa && \
    echo "$ssh_pub_key" > /root/.ssh/id_rsa.pub && \
    chmod 600 /root/.ssh/id_rsa && \
    chmod 600 /root/.ssh/id_rsa.pub

CMD ["/bin/sh", "-c", "eval $(ssh-agent) && ssh-add ~/.ssh/id_rsa && /bin/bash"]
