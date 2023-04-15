class Process():
    def __init__(self) -> None:
        self.code = []
        self.data = {}
        self.pc: int = 0
    
    def read_process(self, filename):
        isCode = False
        isData = False
        with open(filename, 'r') as file:
              for l in file:
                  if l[0:8] == '.enddata':
                      isData = False         
                  if l[0:8] == '.endcode':
                      isCode = False

                  if isData:
                      l_split = l.strip().split()
                      self.data[l_split[0]] = l_split[1] 
                  if isCode:
                      l_split = l.strip().split()

                  if l[0:5] == '.code':
                      isCode = True
                  if l[0:5] == '.data':
                      isData = True
                      # self.code.append()



process = Process()

process.read_process('ex_pgms_tp1/prog3.txt')

print(process.data)

