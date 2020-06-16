db = db.getSiblingDB("covid19");
db.timeseries.find().forEach(function (x) {
	x.date = new Date(x.date - x.date.getTimezoneOffset()*60*1000);
	db.timeseries.save(x);
});