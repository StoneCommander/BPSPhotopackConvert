import os, math

def clear(sym=' '):
  x, y= os.get_terminal_size()
  for i in range(y):
    print(sym*x)
def line(sym=' '):
  x, y= os.get_terminal_size()
  print(sym*x)

def pbar(pcnt,empty=" ",fill="#",size=0,showPcnt=False):
  x, y= os.get_terminal_size()
  if size == 0:
    size = x
  if size < 1:
    size = math.floor(x*size)
  ptxt = f"{round(pcnt*100)}%: "
  if showPcnt: size += -len(ptxt)-1
  numF = math.floor(size*pcnt)
  numE = size-numF
  str = fill*numF + empty*numE
  if showPcnt:
    print(ptxt,str)
  else:
    print(str)  
  

def printF(txt,sym=' ',align='l'):
  x, y= os.get_terminal_size()
  if align.lower()=='c':
    txt = (sym*round((x-len(txt))/2))+txt+(sym*round((x-len(txt))/2))
  elif align.lower()=='r':
    txt = (sym*(x-len(txt)))+txt
  else:
    txt = txt+(sym*(x-len(txt)))
  print(txt)

if __name__ == "__main__":
  print('some random crud')
  clear('=')
  printF('now its clear!','-','r')
  pbar(.5,"_","#")
  pbar(.5,"_","#",0,True)
  pbar(.5,"_","#",20)
  pbar(.5,"_","#",.5)
  pbar(.5,"_","#",.5,True)
  
  