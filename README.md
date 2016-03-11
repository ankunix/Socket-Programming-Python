Author : Ankush Chauhan

Steps to run the system :
Step 1>
  '''
  python router.py
  use --help for all command line options
Step 2>
  '''
  python receiver.py
  replace the argv[1] with the number of packet transmissions
Step 3>
  '''
  python sender.py 100
  replace the argv[1] with the number of packet transmissions

Note unexpected behaviour may occur if number of packets given as argument have a mismatch; no generic checks done.
