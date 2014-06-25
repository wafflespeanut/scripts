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
        l=Math.sqrt(n)-2;
        num= new Array();
        for(i=2; i<= n;i++)
            num.push(i);
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

function keypnum(key) {
	primes=[]
	for(i=0;i<key.length;i++) {
		for(j=1;j<3;j++) {
			primes.push(primelist[Math.pow(key[i].charCodeAt(),j+1)]) } }
	return primes }

function slicing(key) {
	listed=[]; sliced=[]; l=10
	for(i=0;i<key.length;i++)
		{