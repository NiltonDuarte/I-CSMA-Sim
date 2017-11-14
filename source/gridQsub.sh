qsub -e /homesim/nilton.gduarte/error.log -o /homesim/nilton.gduarte/output.log -V -b y -cwd -shell n -q all.q -l hostname=node11 python sim_PROTOCOLO.py 0.01 0.4
qsub -e /homesim/nilton.gduarte/error.log -o /homesim/nilton.gduarte/output.log -V -b y -cwd -shell n -q all.q -l hostname=node11 python sim_PROTOCOLO.py 0.01 0.5
qsub -e /homesim/nilton.gduarte/error.log -o /homesim/nilton.gduarte/output.log -V -b y -cwd -shell n -q all.q -l hostname=node11 python sim_PROTOCOLO.py 0.1 0.4
qsub -e /homesim/nilton.gduarte/error.log -o /homesim/nilton.gduarte/output.log -V -b y -cwd -shell n -q all.q -l hostname=node11 python sim_PROTOCOLO.py 0.1 0.5
qsub -e /homesim/nilton.gduarte/error.log -o /homesim/nilton.gduarte/output.log -V -b y -cwd -shell n -q all.q -l hostname=node11 python sim_PROTOCOLO.py 1 0.4
qsub -e /homesim/nilton.gduarte/error.log -o /homesim/nilton.gduarte/output.log -V -b y -cwd -shell n -q all.q -l hostname=node11 python sim_PROTOCOLO.py 1 0.5

