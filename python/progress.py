

'''
  Print a progress bar to stdout.
'''

import os,sys
import time,datetime

class ProgressBar():

  def __init__(self,N,**kwargs):
    
    self.N_ = int(N) # expected completion point
   
    # process name 
    self.name_ = ''

    # print frequency 
    self.frequency_ = 10

    # parse kwargs
    for k,v in kwargs.iteritems():
      if k == 'name':
    	self.name_ = str(v)
      elif k == 'frequency':
	self.frequency_ = int(v)
    
    self.is_started_ = False
    self.count_ = 0
    self.start_time_ = None

    self.last_count_ = 0


  def dump(self,name,perc,et,eta):
    '''print the current status to stdout.'''

    # construct print string
    pstr = str(name) + ' ' + '[' + '='*int(perc*20) + '-'*int(20*(1-perc)) + ']' + '%.2f%%' % (perc*100.)
    pstr += ' Elapsed: ' + str(datetime.timedelta(seconds=int(et)))
    pstr += ' ETA: ' + str(datetime.timedelta(seconds=int(eta)))

    sys.stdout.write('\r%s' % pstr)
    sys.stdout.flush()

 
  def update(self,n):
    '''Update counters.'''
    
    self.count_ += n

    if not self.is_started_:
      self.is_started_ = True

      self.start_time_ = time.time()


    if self.count_ - self.last_count_ >= self.frequency_:
      elapsed_time = time.time() - self.start_time_
      ETA = float(elapsed_time)/float(self.count_)*(self.N_ - self.count_)

      perc = float(self.count_)/float(self.N_)

      self.dump(self.name_,perc,elapsed_time,ETA)

      self.last_count_ = self.count_


  def complete(self):
    '''Cleanup stdout after prcess complets.'''

    sys.stdout.write('\n')
    sys.stdout.flush()
