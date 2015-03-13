import re
import pycurl
import StringIO

def crawl(address, dir, outputFile):
	try:
		c = pycurl.Curl()  
		c.setopt(pycurl.URL, address)  
		b = StringIO.StringIO()  
		c.setopt(pycurl.WRITEFUNCTION, b.write)  
		c.setopt(pycurl.FOLLOWLOCATION, 1)
		c.setopt(pycurl.TIMEOUT, 30)
		c.perform()
		content = b.getvalue()
		result_merge = re.findall(r'a href=\"/tags/.+?synonyms\" class=\"post-tag\"',content)
		result_synonym = re.findall(r'<a href=\"/questions/tagged/.+?\" class=\"post-tag\" title=\"show questions tagged',content)
		#print len(result_merge)
		merge = []
		synonym = []
		
		for item in result_merge:
			item = re.sub(r'a href=\"/tags/','',item)
			item = re.sub(r'/synonyms\" class=\"post-tag\"','',item)
			merge.append(item)
		
		for item in result_synonym:
			item = re.sub(r'<a href=\"/questions/tagged/', '', item)
			item = re.sub(r'\" class=\"post-tag\" title=\"show questions tagged', '', item)
			synonym.append(item)
		
		fw= open(dir+outputFile,'a')
		for i in range(len(merge)):
			fw.write(synonym[i]+'	'+merge[i]+'\n')
		fw.close()
		
	except Exception, e :
		print e	


def multiCrawl(dir, outputFile):
	for i in range(1,25):
		print i
		address = 'http://stackoverflow.com/tags/synonyms?page='+str(i)+'&tab=synonym&filter=active'
		crawl(address, dir, outputFile)
		
if __name__ == '__main__':
	
	dir = 'D:\\PhD\\code\\python\\webCrawl\\stackOverflow\\'
	f = 'synonymSO.txt'
	
	try:
		#crawl('http://stackoverflow.com/tags/synonyms?page=2&tab=synonym&filter=active', dir, f)
		multiCrawl(dir, f)
		
	except Exception, e :
		print e
		raise	