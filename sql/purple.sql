create table living_things_purple(path ltree, name varchar, display_order varchar);
CREATE INDEX path_gist_idx_p ON living_things_purple USING GIST (path);
CREATE INDEX path_idx_p ON living_things_purple USING BTREE (path);

insert into living_things_purple(display_order, path, name) values ('0', '0', 'Top');

insert into living_things_purple(display_order, path, name) values ('10', 'Top.Fungi', 'Fungi');
insert into living_things_purple(display_order, path, name) values ('20', 'Top.Plant', 'Plant');
insert into living_things_purple(display_order, path, name) values ('30', 'Top.Animal', 'Animal');
insert into living_things_purple(display_order, path, name) values ('40', 'Top.Protista', 'Protista');
insert into living_things_purple(display_order, path, name) values ('50', 'Top.Monera', 'Monera');

insert into living_things_purple(display_order, path, name) values ('10', 'Top.Animal.Molluscs', 'Molluscs');
insert into living_things_purple(display_order, path, name) values ('20', 'Top.Animal.Insects', 'Insects');
insert into living_things_purple(display_order, path, name) values ('30', 'Top.Animal.Mammals', 'Mammals');
insert into living_things_purple(display_order, path, name) values ('21', 'Top.Animal.Birds', 'Birds');


WITH RECURSIVE t AS (
    SELECT t.name
         , t.path
         , 1::int AS lvl
         , t2.display_order AS sort
    FROM   living_things_purple t
    JOIN   living_things_purple t2 ON t2.path = subltree(t.path, 0, 1)

    UNION ALL
    SELECT t.name
         , t.path
         , t.lvl + 1
         , t.sort || t2.display_order
    FROM   t
    JOIN   living_things_purple t2 ON t2.path = subltree(t.path, 0, t.lvl + 1)
    WHERE  nlevel(t.path) > t.lvl
    )
SELECT name, path, max(sort) AS sort
FROM   t
GROUP  BY 1, 2
ORDER  BY max(sort), path;


SELECT t1.name, t1.path, t1.display_order
FROM living_things_purple t1
JOIN living_things_purple t2 ON t2.path = subltree(t1.path, 0, 1)
WHERE t2.
