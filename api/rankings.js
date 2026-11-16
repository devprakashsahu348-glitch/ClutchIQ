const L = require("./_lib");
const data = require("../data/rankings.json");
module.exports = async (req, res) => {
  const u = await L.currentUser(req);
  if (!u) return L.send(res, 401, { error: "Please log in." });
  L.send(res, 200, { ...data, user: { name: u.name } });
};
