INSERT INTO `contact_db`.`contact` (`profile_image_url`, `name`, `email`, `phone`, `company`, `job_title`, `memo`, `address`, `birthday`, `website`)
VALUES
('https://example.com/images/hong.jpg', '홍길동', 'hong@example.com', '01012345678', 'ABC Corp', '개발자', '팀원들과 잘 어울림', '서울시 강남구 테헤란로 123', '1990-01-15', 'https://hong.dev'),
('', '김무개', 'kim@example.com', '01098765432', 'XYZ Inc', '기획자', NULL, '부산시 해운대구 센텀중앙로 456', NULL, ''),
('https://example.com/images/lee.jpg', '이순신', 'lee@naver.com', '01011112222', '해군본부', '장군', '충무공', '전라남도 여수시 이순신로 77', '1545-04-28', 'https://navy.kr'),
('', '최지우', 'choi@gmail.com', '01022223333', '스타트업123', '디자이너', '감각 뛰어남', '경기도 성남시 판교로 333', NULL, 'https://choi.design'),
('https://example.com/images/park.jpg', '박세리', 'seri@korea.com', '01033334444', 'KPGA', '프로골퍼', NULL, '대전광역시 유성구 문화로 89', '1977-09-28', ''),
('', '정우성', 'jung@actor.com', '01044445555', 'A엔터테인먼트', '배우', '광고 모델 다수', '서울 강남구 청담동 88', '1973-03-20', 'https://jungstar.com'),
('', '유재석', 'yu@tv.com', '01055556666', 'MBC', 'MC', '국민MC', '서울 마포구 상암로 238', '1972-08-14', 'https://yoo-ent.com'),
('', '김연아', 'yuna@ice.com', '01066667777', '대한빙상연맹', '피겨선수', '은퇴 후 활동 중', '경기도 군포시 산본로 55', '1990-09-05', ''),
('', '손흥민', 'son@tottenham.com', '01077778888', '토트넘', '축구선수', '잉글리시 프리미어리거', '영국 런던', '1992-07-08', 'https://son7.com'),
('', '배수지', 'suzy@idol.com', '01088889999', 'JYP', '가수/배우', '', '서울 용산구 이태원로 77', '1994-10-10', 'https://suzy.kr');


INSERT INTO `contact_db`.`label` (`name`) VALUES ('중학교');
INSERT INTO `contact_db`.`label` (`name`) VALUES ('고등학교');
INSERT INTO `contact_db`.`label` (`name`) VALUES ('대학교');
INSERT INTO `contact_db`.`label` (`name`) VALUES ('회사');

INSERT INTO `contact_db`.`label_map` (`contact_id`, `label_id`) VALUES ('1', '1');
INSERT INTO `contact_db`.`label_map` (`contact_id`, `label_id`) VALUES ('1', '2');
INSERT INTO `contact_db`.`label_map` (`contact_id`, `label_id`) VALUES ('1', '3');
INSERT INTO `contact_db`.`label_map` (`contact_id`, `label_id`) VALUES ('2', '4');
INSERT INTO `contact_db`.`label_map` (`contact_id`, `label_id`) VALUES ('3', '4');
INSERT INTO `contact_db`.`label_map` (`contact_id`, `label_id`) VALUES ('4', '4');