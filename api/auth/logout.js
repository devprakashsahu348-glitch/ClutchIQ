const L = require("../_lib");
module.exports = (req, res) => { if (!L.guard(req, res, "POST")) return; L.clearCookie(res); L.send(res, 200, { message: "Logged out." }); };
