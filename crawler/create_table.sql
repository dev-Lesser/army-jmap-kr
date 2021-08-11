CREATE table if not exists company  (
        id          INT          NOT NULL AUTO_INCREMENT,
        name        VARCHAR(255)  NOT NULL,
        address     VARCHAR(255),
        phone       VARCHAR(255),
        fax         VARCHAR(255),
        eopjong     VARCHAR(20) NOT NULL,
        product     VARCHAR(20),
        scale       VARCHAR(10) NOT NULL,
    research_field  VARCHAR(10),
    a_number        INT NOT NULL,
    r_number        INT NOT NULL,
    a_enlistment_in INT NOT NULL,
    r_enlistment_in INT NOT NULL,
    a_service       INT NOT NULL,
    r_service       INT NOT NULL,
    latitude        DOUBLE,
    longitude       DOUBLE,
    
    PRIMARY KEY (id)

);