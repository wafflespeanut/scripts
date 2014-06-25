function shift(hand,shift) {
	try {
		newt=[]; s=parseInt(shift)
		for(i=0;i<hand.length;i++) {
			m=hand[i].charCodeAt()+shift
			while(m>255) { m-=255 }
			newt.push(String.fromCharCode(m)) } }
	catch(e) {
		return null }
	return newt.join('') }

function sieve(n) {
	primes=[]
	if(n>=2) {
		l=Math.sqrt(n)-2; num= new Array()
		for(i=2; i<= n;i++)
			num.push(i)
        for(i=0;i<=l;i++) {
			var p=num[i]
			if(p)
				for(j=p*p-2;j<num.length;j+=p)
					num[j]=0; }
		for(i=0;i<num.length;i++) {
			p=num[i];
			if(p)
				primes.push(p); } }
	return primes }

primelist=sieve(512*512)

function hexed(key)	{
	pas=key.split('')
	for(i=0;i<key.length;i++) {
		pas[i]=pas[i].charCodeAt().toString(16) }
	return pas }

function chared(key) {
	pas=[]
	for(i=0;i<key.length;i++) {
		try {
			pas.push(String.fromCharCode(parseInt(key[i],16))) } }
		catch(e) {
			return null }
	return pas.join('') }
	
String.prototype.replaceAt = function(i,ch) {
    return this.substr(0,i) + ch + this.substr(i+ch.length); }

function add(text,key) {
	num="0123456789"; hand=text; i=key.length-1
	for(a=0;a<hand.length;a++) {
		if(i>0 && num.indexOf(hand[a])!=-1) {
			b=(parseInt(hand[a])+key[i].charCodeAt()).toString()
			hand=hand.replaceAt(a,b[b.length-1])
			i-=1 }
		else if(i==0 && num.indexOf(hand[a])!=-1) {
			i=key.length-1
			b=(parseInt(hand[a])+key[i].charCodeAt()).toString()
			hand=hand.replaceAt(a,b[b.length-1])
			i-=1 } }
	return hand }
	
function sub(text,key) {
	num="0123456789"; hand=text; i=key.length-1
	for(a=0;a<hand.length;a++) {
		if(i>0 && num.indexOf(hand[a])!=-1) {
			c=(key[i].charCodeAt()).toString()
			b=(10+parseInt(hand[a])-parseInt(c[c.length-1])).toString()
			hand=hand.replaceAt(a,b[b.length-1])
			i-=1 }
		else if(i==0 && num.indexOf(hand[a])!=-1) {
			i=key.length-1
			c=(key[i].charCodeAt()).toString()
			b=(10+parseInt(hand[a])-parseInt(c[c.length-1])).toString()
			hand=hand.replaceAt(a,b[b.length-1])
			i-=1 } }
	return hand }

function keypnum(key,level) {
	primes=[]
	for(i=0;i<key.length;i++) {
		primes.push(primelist[key[i].charCodeAt()]) }
	for(n=1;n<=level;n++) {
		temp=[]; temp+=primes
		for(i=0;i<temp.length;i++) {
			primes.push(primelist[temp[i]]) } }
	return primes }
	
function pop(key,level) {
	merged=[]; listed=keypnum(key,level)
	for(i=1;i<=level;i++) {
		listed.push(keypnum((listed).join(''),level)) }
	p=listed.join('')
	while(p.length>=10) {
		merged.push(p.substr(0,10))
		p=p.substr(10) }
	return merged }

function find(text,key,level) {
	listed=pop(key,level)
	for(i=0;i<listed.length;i++) {
		if extract(extract(text,listed[i]),key)!=null {
			return extract(text,listed[i]) }
		else { continue } }
	return null }

function combine(text,key) {
	try {
		pas=hexed(key); phrase=hexed(text)
		primes=sieve(Math.pow(key.length,2))
		i=0; ph=phrase.length; p=key.length
		for(j=0;j<pas.length;j++) {
			if(primes[i]<phrase.length) {
				phrase=phrase.substr(0,primes[i])+j+phrase.substr(primes[i])
				i+=1 }
			else { break } } }
	catch(e) {
		return null }
	phr=add(phrase,key)
	return phr.join('')

function extract(text,key) {
	try {
		phrase=chared(sub(text,key));
		primes=sieve(Math.pow(key.length,2))
		ph=phrase.length; newph=""
		for(i=0;i<ph;i++) {
			if((primes.substr(0,key.length)).indexOf(i)==-1) {
				newph.push(phrase[i])
	catch(e) {
		return null }
	return newph.join('')

function eit(text,key,level) {
	i=1; combined=combine(text,key)
	p=pop(key,level); /* RANDOM */
	while(i<level) {
		combined=combine(combined,key); i+=1 }
	if(i==level || level==0) {
		combined=combine(combined, /* RANDOM */) }
	if(combined==null) {
		return null }
	zombie=combined
	for(i=0;i<key.length;i++)
		zombie=shift(zombie,key[i].charCodeAt())
	return hexed(zombie).join()

function dit(text,key,level) {
	zombie=chared(text)
	for(i=0; i<key.length; i++)
		zombie=shift(zombie,255-key[i].charCodeAt())
	i=1; extracted=find(zombie,key,level)
	if(level==0)
		extracted=extract(extracted,key)
	while(i<level) {
		extracted=extract(extracted,key); i+=1 }
	if(i==level)
		extracted=extract(extracted,key)
	if(extracted==null)
		return null
	return extracted