import daemon
from label_propagation import LocalGraph

with daemon.DaemonContext(chroot_directory=None, working_directory='./'):
    lg = LocalGraph()
    lg.generate_from_user("animesh_garg")