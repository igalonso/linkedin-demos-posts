CREATE DATASET `gen-ai-igngar`.`supermarket`;

CREATE or replace TABLE `gen-ai-igngar`.`supermarket`.`supermarket-skus`  (
  id INT64 NOT NULL,
  source_id STRING NOT NULL,
  sku STRING NOT NULL,
  brand STRING NOT NULL,
  category STRING NOT NULL,
  name STRING NOT NULL,
  price FLOAT64 NOT NULL,
  currency STRING NOT NULL,
  image_url STRING,
  metadata JSON
);

INSERT INTO `gen-ai-igngar`.`supermarket`.`supermarket-skus` 
(id, source_id, sku, brand, category, name, price, currency, image_url, metadata)
VALUES
(1,'src001','SKU-001','Generic','Dairy','BUTTER',3.50,'EUR','https://www.allrecipes.com/thmb/YEHvUygNdvsUwzKttGh314d9n1M=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/sticks-of-butter-photo-by-twoellis-GettyImages-149134517-resized-3911123142a141eca2340a4bb63e0869.jpg', PARSE_JSON('{"size":"250g"}')),
(2,'src001','SKU-002','Generic','Dairy','BUTTER',3.99,'EUR','https://i5.walmartimages.com/seo/Great-Value-Salted-Butter-Sticks-8-oz-2-Sticks_2a0259b0-1540-49b6-953b-2f4b35b2f1b7.2e62dbdb3d26a5b61d463e9e8f21bb89.jpeg', PARSE_JSON('{"size":"500g"}')),
(3,'src001','SKU-003','Generic','Dairy','BUTTER',4.25,'EUR','https://assets.iceland.co.uk/i/iceland/just_like_butter_1kg_54526_T1.jpg', PARSE_JSON('{"size":"1kg"}')),
(4,'src002','SKU-004','Kellogs','Snacks','GRANOLA',4.99,'EUR','https://images.kglobalservices.com/www.kelloggs.co.za/en_za/product/product_969490/prod_img-1428240_za_06009710890516_2204262015_p_1.png', PARSE_JSON('{"size":"300g"}')),
(5,'src002','SKU-005','Granola Brand','Snacks','GRANOLA',5.49,'EUR','https://example.com/granola-bacon2.jpg', PARSE_JSON('{"size":"500g"}')),
(6,'src003','SKU-006','Pastoret','Dairy','GREEK YOGURT SKIMMED',2.00,'EUR','https://example.com/greek-yogurt.jpg', PARSE_JSON('{"size":"500g"}')),
(7,'src004','SKU-007','Generic','Bakery','SNACK BREAD Regañas',1.75,'EUR','https://example.com/bread.jpg', PARSE_JSON('{"quantity":"1 loaf"}')),
(8,'src005','SKU-008','Generic','Grains','OATS',1.25,'EUR','https://example.com/rolled-oats.jpg', PARSE_JSON('{"size":"500g"}')),
(9,'src006','SKU-009','Generic','Dairy','MILK',2.50,'EUR','https://example.com/milk-carton.jpg', PARSE_JSON('{"volume":"1L"}')),
(10,'src007','SKU-010','Protein Brand','Supplements','PROTEIN POWDER',24.99,'EUR','https://example.com/protein-powder.jpg', PARSE_JSON('{"size":"1kg"}')),
(11,'src008','SKU-011','Generic','Dairy','CHEESE',4.25,'EUR','https://www.dairyfoods.com/ext/resources/2012_January/2012-October/dfx1012-cheese-Bel2-slide.jpg', PARSE_JSON('{"size":"200g"}')),
(12,'src009','SKU-012','Pest Brand','Household','ANT EATER TRAPS',8.99,'EUR','https://example.com/ant-trap.jpg', PARSE_JSON('{"quantity":"1"}')),
(13,'src010','SKU-013','Generic','Produce','BERRIES',3.50,'EUR','https://example.com/berries.jpg', PARSE_JSON('{"size":"250g"}')),
(14,'src010','SKU-014','Generic','Produce','BERRIES',3.99,'EUR','https://example.com/berries2.jpg', PARSE_JSON('{"size":"500g"}')),
(15,'src011','SKU-015','Generic','Produce','OLIVES',2.75,'EUR','https://example.com/olives-jar.jpg', PARSE_JSON('{"size":"300g"}')),
(16,'src012','SKU-016','Generic','Produce','JALAPENO',0.80,'EUR','https://example.com/jalapeno-pepper.jpg', PARSE_JSON('{"quantity":"5"}')),
(17,'src013','SKU-017','Fish Brand','Seafood','FISH FINGERS',5.49,'EUR','https://example.com/fish-fingers.jpg', PARSE_JSON('{"size":"400g"}')),
(18,'src014','SKU-018','Cheese Brand','Dairy','FINGER CHEESE',3.99,'EUR','https://example.com/cheese-sticks.jpg', PARSE_JSON('{"quantity":"10"}')),
(19,'src015','SKU-019','Generic','Poultry','CHICKEN',7.99,'EUR','https://example.com/chicken.jpg', PARSE_JSON('{"size":"1kg"}')),
(20,'src015','SKU-020','Generic','Poultry','CHICKEN',8.50,'EUR','https://example.com/chicken2.jpg', PARSE_JSON('{"size":"1.5kg"}')),
(21,'src016','SKU-021','Dompastick','Seafood','SALMON',10.99,'EUR','https://example.com/salmon-fillet.jpg', PARSE_JSON('{"size":"500g"}')),
(22,'src017','SKU-022','Generic','Seafood','COD',8.50,'EUR','https://example.com/cod.jpg', PARSE_JSON('{"size":"500g"}')),
(23,'src018','SKU-023','Generic','Minerals','BORON',12.99,'EUR','https://example.com/boron-supplement.jpg', PARSE_JSON('{"quantity":"60 capsules"}')),
(24,'src019','SKU-024','Pan Brand','Kitchenware','FRYING PANS',20.00,'EUR','https://example.com/frying-pan.jpg',PARSE_JSON('{"quantity":"1"}')),
(25,'src020','SKU-025','Generic','Meat','MEAT',12.50,'EUR','https://example.com/steak.jpg', PARSE_JSON('{"size":"500g"}')),
(26,'src021','SKU-026','Generic','Meat','PORK CHOPS',6.99,'EUR','https://example.com/pork-chops.jpg', PARSE_JSON('{"type": "bone-in", "size": "300g"}')),
(27,'src021','SKU-027','Generic','Meat','PORK TENDERLOIN',8.99,'EUR','https://example.com/pork-tenderloin.jpg', PARSE_JSON('{"size": "500g"}')),
(28,'src022','SKU-028','Butcher Brand','Meat','LAMB CHOPS',11.99,'EUR','https://example.com/lamb-chops.jpg', PARSE_JSON('{"size": "400g"}')),
(29,'src022','SKU-029','Butcher Brand','Meat','LEG OF LAMB',18.99,'EUR','https://example.com/leg-of-lamb.jpg', PARSE_JSON('{"size": "1.5kg"}')),
(30,'src023','SKU-030','Generic','Meat','VENISON STEAKS',14.99,'EUR','https://example.com/venison.jpg', PARSE_JSON('{"size": "400g"}')),
(31,'src024','SKU-031','Generic','Meat','GOAT MEAT',10.99,'EUR','https://example.com/goat.jpg', PARSE_JSON('{"size": "500g", "cut": "stew meat"}')),
(32,'src025','SKU-032','Specialty Brand','Meat','VEAL CUTLETS',13.50,'EUR','https://example.com/veal.jpg', PARSE_JSON('{"size": "300g"}'));