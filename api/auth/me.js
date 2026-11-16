const L = require("../_lib");
module.exports = async (req, res) => {
  const u = await L.currentUser(req);
  if (!u) return L.send(res, 401, { error: "Not signed in." });
  L.send(res, 200, { name: u.name, email: u.email });
};
