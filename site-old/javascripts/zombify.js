function test(phr) {
	str=hexed(chared(phr)).join('');
	banlist="123456789abcdef"
	for(i=0;i<str.length;i++) {
		if(parseInt(str[i])==0 && banlist.indexOf(str[i-1])==-1)
			return false }
	return true }

function shift(hand,shift) {
		newt=[]; s=parseInt(shift)
		for(i=0;i<hand.length;i++) {
			m=hand[i].charCodeAt()+shift
			while(m>255) { m-=255 }
			newt.push(String.fromCharCode(m)) }
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

function primelist(level) {
	k=Math.pow(2,3+level)
	return sieve(k*k) }

function hexed(key)	{
	pas=key.split('')
	for(i=0;i<key.length;i++) {
		pas[i]=pas[i].charCodeAt().toString(16) }
	return pas }

function chared(key) {
	pas=[]; keyc=[]; m=0
	while(m<key.length) {
		keyc.push(subarr(key,m,m+2).join(''))
		m+=2 }
	for(i=0;i<keyc.length;i++)
		pas.push(String.fromCharCode(parseInt(keyc[i],16)))
	return pas.join('') }

String.prototype.replaceAt = function(i,ch) {
    return this.substr(0,i) + ch + this.substr(i+ch.length); }

function dupe(arr) {
	return arr.filter(function(elem, pos) {
		return arr.indexOf(elem) == pos }) }

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

function keypnum(key) {
	primes=[]; plist=primelist(3)
	for(i=0;i<key.length;i++) {
		primes.push(plist[key[i].charCodeAt()]) }
	for(n=1;n<=2;n++) {
			temp = []
		for(i=0;i<primes.length;i++)
			temp.push(primes[i])
		for(i=0;i<temp.length;i++)
			primes.push(plist[temp[i]]) }
	return primes }
	
function pop(key) {
	merged=[]; listed=keypnum(key); k=0
	p=listed.join(''); n=8
	while(p.length>=n) {
		merged.push(p.substr(0,n))
		p=p.substr(n) }
	for(i=0;i<key.length;i++) {
		k+=parseInt(dupe(merged)[key[i].charCodeAt()]) }
	return k.toString() }

function combine(text,key) {
	phrase=text
	primes=sieve(Math.pow(key.length,2))
	i=0; ph=phrase.length;
	for(j=0;j<key.length;j++) {
		if(primes[i]<phrase.length) {
			phrase=phrase.substr(0,primes[i])+key[j]+phrase.substr(primes[i])
			i+=1 }
	else { break } }
	phr=add(hexed(phrase).join(''),key)
	return phr }

function subarr(arr,index,length) {
	newarr=[]
	for(i=index;i<length;i++) {
		newarr.push(arr[i]) }
	return newarr }
	
function extract(text,key) {
		phrase=chared(sub(text,key));
		primes=subarr(sieve(Math.pow(key.length,2)),0,key.length)
		ph=phrase.length; newp=[]
		for(i=0;i<ph;i++) {
			if(primes.indexOf(i)==-1) {
				newp.push(phrase[i]) }}
	return newp.join('') }

function eit(text,key) {
	combined=combine(text,key);
	rkey=combine(pop(key),key)
	zombie=combine(combine(combined,key),rkey)
	for(i=0;i<key.length;i++)
		zombie=shift(zombie,key[i].charCodeAt())
	return hexed(zombie).join('') }

function dit(text,key) {
	zombie=chared(text)
	for(i=0; i<key.length; i++)
		zombie=shift(zombie,255-(key[i].charCodeAt()))
	rkey=combine(pop(key),key)
	extracted=extract(extract(zombie,rkey),key)
	return extract(extracted,key) }