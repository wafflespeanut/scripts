function atmos(alt) {
	function temp(value, slope, hmin, hmax) {
		return value + slope * (hmax - hmin)
	}

	function pres(value, t, t0, slope) {
		return value * (Math.pow((t / t0), (-g / (slope * R))))
	}

	function cons(value, t, hmin, hmax) {
		return value * (Math.exp(-g / (R * t) * (hmax - hmin)))
	}

	function dens(value, t, t0, slope) {
		return value * (Math.pow((t / t0), (-g / (slope * R) - 1)))
	}

	// constants
	g = 9.80665; R = 287;
	// ground level values
	t0 = 288.15; p0 = 101325; d0 = p0 / (R * t0);
	// temperature slopes
	a01 = -0.0065; a23 = 0.001; a34 = 0.0028;
	// temperature
	t1 = temp(t0, a01, 0, 11000);
	t2 = t1; // constant slope
	t3 = temp(t2, a23, 20000, 32000);
	t4 = temp(t3, a34, 32000, 47000);
	// pressure
	p1 = pres(p0, t1, t0, a01);
	p2 = cons(p1, t2, 11000, 20000);
	p3 = pres(p2, t3, t2, a23);
	// density
	d1 = dens(d0, t1, t0, a01);
	d2 = cons(d1, t2, 11000, 20000);
	d3 = dens(d2, t3, t2, a23);

	if (alt == 0) {
		te = t0;
		pr = p0;
		de = d0;
	} else if (alt > 0 && alt <= 11000) {
		te = temp(t0, a01, 0, alt);
		pr = pres(p0, te, t0, a01);
		de = dens(d0, te, t0, a01);
	} else if (alt > 11000 && alt <= 20000) {
		te = t1;
		pr = cons(p1, te, 11000, alt);
		de = cons(d1, te, 11000, alt);
	} else if (alt > 20000 && alt <= 32000) {
		te = temp(t2, a23, 20000, alt);
		pr = pres(p2, te, t2, a23);
		de = dens(d2, te, t2, a23);
	} else if (alt > 32000 && alt <= 47000) {
		te = temp(t3, a34, 32000, alt);
		pr = pres(p3, te, t3, a34);
		de = dens(d3, te, t3, a34);
	} else {
		return ["undefined", "undefined", "undefined"]
	}

	return [Math.round(pr * 10000) / 10000,
			Math.round(te * 10000) / 10000,
			Math.round(de * 10000) / 10000]
}
