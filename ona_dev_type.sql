USE ona_default_11;
SELECT t.id "ID", v.name "Manufacturer", m.name"Model", r.name "Role"
FROM device_types t
INNER JOIN models m
ON t.model_id = m.id
INNER JOIN roles r
ON t.role_id = r.id
INNER JOIN manufacturers v
ON m.manufacturer_id = v.id;