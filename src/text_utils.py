#!/usr/bin/python2.5
# -*- coding: utf-8 -*-
##   text_utils.py 
##
##   Copyright © 2008-2010 Saeed Rasooli <saeed.gnu@gmail.com>  (ilius)
##
##   This program is a free software; you can redistribute it and/or modify
##   it under the terms of the GNU General Public License as published by
##   the Free Software Foundation; either version 3, or (at your option)
##   any later version.
##
##   You can get a copy of GNU General Public License along this program
##   But you can always get it from http://www.gnu.org/licenses/gpl.txt
##
##   This program is distributed in the hope that it will be useful,
##   but WITHOUT ANY WARRANTY; without even the implied warranty of
##   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See  the
##   GNU General Public License for more details.

import string, re, sys, os, subprocess
##from  xml.etree.ElementTree import XML, tostring  ## used for xml2dict

startRed	= '\x1b[31m'
endFormat	= '\x1b[0;0;0m'		# End Format		#len=8

## ascii spacial characters.
schAs=["\n", ",", ".", "[", "]", "(", ")", '-', '+', '=', '/', '\\',
',', ':', ';', "'", '"', '`', '_', '!', '?', '*', '@', '#']

digitsFa=['۰','۱','۲','۳','۴','۵','۶','۷','۸','۹']

## persian spacial characters.
schFa=[
'\xd8\x9b', '\xd8\x9f','\xe2\x80\xa6','\xc2\xab','\xc2\xbb','\xd9\x80','\xd9\x94','\xd8\x8c' ,'\xe2\x80\x93','\xe2\x80\x9c','\xe2\x80\x9d','\xe2\x80\x8c']
commaFa='\xd8\x8c'

## other unicode spacial characters.
schUn=['\xee\x80\x8a','\xee\x80\x8c']

#for ch in schFa + schUn :
#  print(ch)
sch = schAs+schFa+schUn+list(string.whitespace)+list(string.digits)+digitsFa

"""
myPrint = sys.stdout.write

def textProgress(n=100, t=0.1):
  import time
  for i in xrange(n):
    myPrint('\b\b\b\b##%3d'%(i+1));time.sleep(t)
  myPrint('\b\b\b')

def locate(lst, val):
 n=len(lst)
 if n==0:
  return
 if val < lst[0]:
  return -0.5
 if val == lst[0]:
  return 0
 if val == lst[-1]:
  return n-1
 if val > lst[-1]:
  return n-0.5
 si=0 # start index
 ei=n # end index
 while ei-si>1:
  mi=(ei+si)/2 # middle index
  if lst[mi] == val :
   return mi
  elif lst[mi] > val :
   ei=mi
   continue
  else:
   si=mi
   continue
 if ei-si==1:
  return si+0.5

def locate2(lst, val, ind=1):
 n=len(lst)
 if n==0:
  return
 if val<lst[0][ind]:
  return -0.5
 if val==lst[0][ind]:
  return 0
 if val==lst[-1][ind]:
  return n-1
 if val>lst[-1][ind]:
  return n-0.5
 si=0
 ei=n
 while ei-si>1:
  mi=(ei+si)/2
  if lst[mi][ind]==val:
   return mi
  elif lst[mi][ind]>val:
   ei=mi
   continue
  else:
   si=mi
   continue
 if ei-si==1:
  return si+0.5

def xml2dict(xmlText):
  from  xml.etree.ElementTree import XML, tostring
  xmlElems = XML(xmlText)
  for elem in xmlElems:
    elemText=tostring(elem)
    try:
      elem[0]
      elemElems=xml2dict()
    except:
      pass
"""

def printAsError(text='An error occured!', exit=False):
  sys.stderr.write('%s\n'%text)
  if exit:
    sys.exit(1)


def myRaise(File=None):
  i = sys.exc_info()
  if File==None:
    sys.stderr.write('line %s: %s: %s'%(i[2].tb_lineno, i[0].__name__, i[1]))
  else:
    sys.stderr.write('File "%s", line %s: %s: %s'%(File, i[2].tb_lineno, i[0].__name__, i[1]))

def timeHMS(seconds):
  (h, m, s)=time.gmtime(int(seconds))[3:6]
  if h==0:
    if m==0:
      return '%.2d'%s
    else:
      return '%.2d:%.2d'%(m, s)
  else:
    return '%.2d:%.2d:%.2d'%(h, m, s)


def addDefaultOptions(opt, defOpt, escapeList=[None,'Unknown','unknown']):
  # Two varable opt(meaning options) and defOpt(meaning defaults options) have dict type.
  # this function sets options to defaults if they have not defined 
  # or have special values (in escapeList)
  # modifies opt variable an reuturns nothing
  for item in defOpt.keys():
    if item in opt.keys():
      if not opt[item] in escapeList:
        continue
    opt[item] = defOpt[item]

def mergeLists(lists):
  if not isinstance(lists, (list, tuple)):
    raise TypeError('bad type given to mergeLists: %s'%type(lists))
  """
  for i in xrange(len(lists)):
    item = lists[i]
    if not isinstance(item, (list, tuple)):
      raise TypeError, 'argument give to mergeLists() at index %d is: \'%s\' ,bad type: \'%s\'' % (i, item, type(item))
  """
  if len(lists)==0:
    return []
  elif len(lists)==1:
    if isinstance(lists[0], (list, tuple)):
      return lists[0][:]
    else:
      return lists[0]
  else:
    return lists[0]+mergeLists(lists[1:])

def findAll(st, sub):
  ind = []
  if isinstance(sub, basestring):
    i = 0
    sbl = len(sub)
    while True:
      i = string.find(st, sub, i)
      if i==-1:
        break
      ind.append(i)
      i += sbl
  elif isinstance(sub, (list, tuple)):
    for item in sub:
      ind += findAll(st, item)
    ind.sort()
  else:
    print('Invailed second argument to function findAll!')
    return []
  return ind

"""
def sortby(lst, n, reverse=False):
  nlist = [(x[n], x) for x in lst]
  nlist.sort(None, None, reverse)
  return [val for (key, val) in nlist]


def sortby_inplace(lst, n, reverse=False):
  lst[:] = [(x[n], x) for x in lst]
  lst.sort(None, None, reverse)
  lst[:] = [val for (key, val) in lst]
  return
"""

def checkOrder(lst):
 wrong = []
 for i in xrange(len(lst)-1):
   if lst[i] == lst[i+1]:
     wrong.append(i)
 return wrong

def removeRepeats(lst):
  ## gets a sorted list and removes any reapeated member. returns result.
  n=len(lst)
  if n==0:
    return []
  lstR=[lst[0]]
  for i in xrange(1,n):
    if lst[i] != lst[i-1]:
      lstR.append(lst[i])
  return lstR

def addWord(word, allWords):
    if len(allWords)==0: 
      return [word]
    i=locate(allWords,word)
    ii=int(i+1)
    if ii-i==0.5:
      allWords.insert(ii,word)
    return allWords

def findWords(st0, opt={}):
   # take all words of a text
   # and returns their indexes as a list.
   defOpt = {'minLen':3, 'noEn':True}
   addDefaultOptions(opt, defOpt)
   st = st0[:]
   ind = []
   for ch in sch:
     st = st.replace(ch,' '*len(ch))
   if len(st)!=len(st0):
     print('Error in function text_utlis.findWord. string length has been changed!')
     return []
   si = [-1] + findAll(st, ' ') + [len(st)] # separatior indexes
   for i in xrange(len(si)-1):
     word = st[si[i]+1:si[i+1]]
     if word.strip()=='':
       continue
     if 'word' in opt.keys():
       if word != opt['word']:
         continue
     if len(word) < opt['minLen']:
       continue
     if opt['noEn']:
       en = False
       for c in word:
         if c in string.printable:
           en = True
       if en:
         continue
     ind.append( [ si[i]+1 , si[i+1] ] )
   return ind

def takeStrWords(st, opt={}):
   # take all words of a text
   # and returns them as a list of strings.
   defOpt = {'minLen':3, 'noEn':True, 'sort':True, 'noRepeat':True}
   addDefaultOptions(opt, defOpt)
   words = [ st[i:j] for [i,j] in findWords(st, opt) ]
   # 'sort' and 'noRepeat' options will not be used in findWords()
   if opt['sort']:
     words.sort()
   if opt['noRepeat']:
     words = removeRepeats(words)
   return words

def takeFileWords(filePath, opt={'minLen':3, 'sort':True, 'noRepeat':True}):
  try:
    fp = open(filePath,'r')
  except:
    print('Can not open file',filePath)
  return takeStrWords(fp.read(), opt)


def removeTextTags(st, tags):
  if 'p' in tags:
    st.replace('<p', '\n<p')
  if 'P' in tags:
    st.replace('<P', '\n<P')
  for tag in tags.keys():
    removeBetween = tags[tag]
    tl = len(tag)
    i0=0
    while True:
      i1 = st.find('<%s'%tag, i0)
      if i1==-1:
        break
      try:
        c = st[i1+tl+1]
      except IndexError:
        break
      if c=='>':
        i2 = i1+tl+1
      elif c==' ':
        i2 = st.find('>', i1+1)
        if i2==-1:
          i0 = i1+1
          continue
      elif c=='/':
        i2 = st.find('>', i1+1)
        if i2==-1:
          i0 = i1+1
          continue
        elif i2==i1+tl+2:
          removeBetween = False
      else:
        i0 = i1 + tl #??????
        continue
      i3 = st.find('</%s>'%tag, i2)
      if i3==-1:
        st = st[:i1] + st[i2+1:]
        i0 = i1 + 1
        #if tag=='A':
        #  printAsError('tag "A" closing not found!')
        continue
      i4 = i3 + tl + 3 # i3 + len('</%s>'%tag) # must not +1
      if removeBetween:
        #if i4 >= len(st):
        #  st = st[:i1]
        #  break
        st = st[:i1] + st[i4:]
        i0 = i1 + 1
      else:
        st = st[:i1] + st[i2+1:i3] + st[i4:]
        i0 = i1 + i3 - i2 + 1 # is +1 needed???????
      #print i0, i1, i2, i3
      st = st.replace('<%s>'%tag, '').replace('</%s>'%tag, '')
  return st


def replaceInFileAs2Files(inF, fromF, toF, outName):
  lines1 = fromF.readlines()
  lines2 = toF.readlines()
  n = min(len(lines1), len(lines2))
  rpl = []
  for i in xrange(n):
    if lines1[i] != lines2[i]:
      rpl.append([ lines1[i][:-1], lines2[i][:-1] ])
  del lines1, lines2
  text = inF.read()
  for item in rpl:
    text = text.replace(item[0], item[1])
  outF = open(outName)
  outF.write(text)
  outF.close()
  del text, outF


def relation(word, phrase, opt={}):## FIXME
  defOpt={'sep':commaFa, 'matchWord':True}
  addDefaultOptions(opt, defOpt)
  if phrase.find(word)==-1:
    return 0.0
  phraseParts = phrase.split(opt['sep'])
  rel=0.0 #relationship value of word to pharse(as a float number between 0 and 1
  for part0 in phraseParts:
    for ch in sch:
      part=part0.replace(ch,' ')
    pRel = 0 # part relationship
    if opt['matchWord']:
       pNum = 0
       partWords = takeStrWords(part)
       pLen = len(partWords)
       if pLen==0:
         continue
       for pw in partWords:
         if pw==word:
           pNum += 1
       pRel=float(pNum)/pLen  # part relationship
    else:
       pLen = len(part.replace(' ',''))
       if pLen==0:
         continue
       pNum = len(findAll(part, st)*len(st))
       pRel=float(pNum)/pLen  # part relationship
    if pRel > rel:
      rel = pRel
    #del pRel
  return rel

def charDigToInt(ch):
  if not isinstance(ch, basestring):
    raise RuntimeError('bad argument given to charDigToInt: "%s" must be a one length string.'%ch)
  elif len(ch)!=1:
    raise RuntimeError('bad argument given to charDigToInt: "%s" must be a one length string.'%ch)
  elif '0'<=ch<='9':
    return ord(ch)-48 #int(ch)
  elif 'a'<=ch<='z':
    return ord(ch)-87
  elif 'A'<=ch<='Z':
    return ord(ch)-55
  else:
    raise RuntimeError('bad argument given to charDigToInt: "%s"'%ch)
    

def intToBinStr0(n, stLen=0):
  if not isinstance(stLen, int):
    raise TypeError('bad type second argument given to intToBinStr: "%s"'%type(stLen))
  h=hex(n)
  if h[-1]=='L':
    h = h[2:-1]
  else:
    h = h[2:]
  if len(h)%2==1:
    h='0'+h
  bs = ''
  for i in xrange(0, int(len(h)), 2):
    bs += chr( 16*charDigToInt(h[i]) + charDigToInt(h[i+1]) )
  bsl = len(bs)
  if bsl<stLen:
    bs = '\x00'*(stLen-bsl) + bs
  return bs

def intToBinStr(n, stLen=0):
  bs = ''
  while n>0:
    bs = chr(n & 255) + bs
    n = n >> 8
  bsl = len(bs)
  if bsl<stLen:
    bs = '\x00'*(stLen-bsl) + bs
  return bs


def binStrToInt(bs):
  l = len(bs)
  return sum([ ord(bs[i]) * (256**(l-1-i)) for i in xrange(l) ])


def chBaseIntToStr(number, base):
    """intToStr( number, base ) -- reverse function to int(str,base) and long(str,base)"""
    if not 2 <= base <= 36:
      raise ValueError('base must be in 2..36')
    abc = string.digits + string.letters
    result = ''
    if number < 0:
      number = -number
      sign = '-'
    else:
      sign = ''
    while True:
      number, rdigit = divmod( number, base )
      result = abc[rdigit] + result
      if number == 0:
         return sign + result

def chBaseIntToList(number, base):
    result = []
    if number < 0:
      raise ValueError('number must be posotive integer')
    while True:
      number, rdigit = divmod( number, base )
      result = [rdigit] + result
      if number == 0:
         return result


def recodeToWinArabic(s):
  u = s.decode('utf8', 'replace')
  replaceList=[(u'ی',u'ي'),(u'ک',u'ك'),(u'ٔ',u'ء'),('\xef\xbf\xbd','')]+[(unichr(i),unichr(i+144)) for i in xrange(1632,1642)]
  for item in replaceList:
    u = u.replace(item[0], item[1])
  try:
    return u.encode('windows-1256', 'replace')
  except:
    printAsError('can not encode string "%s" into windows-1256(arabic windows)'%s)
    return ''



def urlToPath(url):
  if len(url)<7:
    return url
  if url[:7]!='file://':
    return url
  path=url[7:]
  if path[-2:]=='\r\n':
    path=path[:-2]
  elif path[-1]=='\r':
    path=path[:-1]
  ## here convert html unicode symbols to utf8 string:
  if not '%' in path:
    return path
  path2=''
  n=len(path)
  i=0
  while i<n:
    if path[i]=='%' and i<n-2:
      path2 += chr(eval('0x%s'%path[i+1:i+3]))
      i += 3
    else:
      path2 += path[i]
      i += 1
  return path2



replacePostSpaceChar = lambda st, ch: st.replace(' '+ch, ch).replace(ch, ch+' ').replace(ch+'  ', ch+' ')

def faEditStr(st):
  return replacePostSpaceChar(
            st.replace('ي', 'ی')\
              .replace('ك', 'ک')\
              .replace('ۂ', 'هٔ')\
              .replace('ہ', 'ه')\
         , '،')



def my_url_show(link):
  for path in ('/usr/bin/gnome-www-browser','/usr/bin/firefox','/usr/bin/iceweasel','/usr/bin/konqueror'):
    if os.path.isfile(path):
      subprocess.call([path, link])
      break
"""
try:
  from gnome import url_show
except:
  try:
    from gnomevfs import url_show
  except:
    url_show = my_url_show
"""
def click_website(widget, link):
  my_url_show(link)

def runDictzip(filename):
  dictzipCmd = '/usr/bin/dictzip' ## Save in pref ## FIXME
  if not os.path.isfile(dictzipCmd):
    return False
  if filename[-4:]=='.ifo':
    filename = filename[:-4]
  (out, err) = subprocess.Popen(
    [dictzipCmd, filename+'.dict'],
    stdout=subprocess.PIPE
  ).communicate()
  #out = p3[1].read()
  #err =  p3[2].read()
  #print('dictzip command: "%s"'%dictzipCmd)
  #if err:
  #  printAsError('dictzip error: %s'%err.replace('\n', ' '))
  #if out!='':
  #  print('dictzip error: %s'%out.replace('\n', ' '))



