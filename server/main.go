package main

import (
	"database/sql"
	"fmt"
	"log"
	"net/http"

	"github.com/gin-gonic/gin"
	_ "github.com/go-sql-driver/mysql"
)

var db *sql.DB

type Company struct {
	Id              int            `json:"id"`
	Name            string         `json:"name"`
	Address         string         `json:"address"`
	Phone           string         `json:"phone"`
	Fax             string         `json:"fax"`
	Eopjong         string         `json:"eopjong"`
	Product         string         `json:"product"`
	Scale           string         `json:"scale"`
	Research_field  string         `json:"rfield"`
	A_number        int            `json:"a_number"`
	R_number        int            `json:"r_number"`
	A_enlistment_in int            `json:"a_enlistment_in"`
	R_enlistment_in int            `json:"r_enlistment_in"`
	A_service       int            `json:"a_service"`
	R_service       int            `json:"r_service"`
	Latitude        sql.NullString `json:"latitude"`
	Longitude       sql.NullString `json:"longitude"`
}

func (p Company) get(sid string) (companies []Company, err error) {

	rows, _ := db.Query("SELECT id, name, address, latitude, longitude FROM company LIMIT 40 OFFSET ?", sid)

	for rows.Next() {
		var company Company
		err := rows.Scan(&company.Id, &company.Name, &company.Address,
			&company.Phone,
			&company.Fax,
			&company.Eopjong,
			&company.Product,
			&company.Scale,
			&company.Research_field,
			&company.A_number,
			&company.R_number,
			&company.A_enlistment_in,
			&company.R_enlistment_in,
			&company.A_service,
			&company.R_service,
			&company.Latitude, &company.Longitude)
		if err != nil {
			log.Fatal(err)
		}
		companies = append(companies, company)
	}
	if err != nil {
		return
	}
	return
}

func (p Company) getName(name string) (companies []Company, err error) {
	query := fmt.Sprintf("SELECT id, name, address, latitude, longitude FROM company WHERE name LIKE '%% %s %%'", name)

	rows, _ := db.Query(query)

	for rows.Next() {
		var company Company
		err := rows.Scan(&company.Id, &company.Name, &company.Address, &company.Latitude, &company.Longitude)
		if err != nil {
			log.Fatal(err)
		}
		companies = append(companies, company)
	}
	if err != nil {
		return
	}
	return
}
func (p Company) getAll() (companies []Company, err error) {
	rows, err := db.Query("SELECT * FROM company")
	if err != nil {
		panic(err)
	}
	for rows.Next() {
		var company Company
		err := rows.Scan(&company.Id, &company.Name, &company.Address,
			&company.Phone,
			&company.Fax,
			&company.Eopjong,
			&company.Product,
			&company.Scale,
			&company.Research_field,
			&company.A_number,
			&company.R_number,
			&company.A_enlistment_in,
			&company.R_enlistment_in,
			&company.A_service,
			&company.R_service,
			&company.Latitude, &company.Longitude)
		if err != nil {
			log.Fatal(err)
		}
		companies = append(companies, company)
	}
	defer rows.Close()
	return
}

func main() {
	var err error
	db, err = sql.Open("mysql", "user:user1234@tcp(localhost:13306)/company?parseTime=true") // TODO dotenv 로 바꿔야함
	if err != nil {
		log.Fatal(err.Error())
	}
	defer db.Close()

	err = db.Ping()
	if err != nil {
		log.Fatal(err.Error())
	}

	router := gin.Default()

	router.GET("/companies", func(c *gin.Context) {
		p := Company{}
		companies, err := p.getAll()
		if err != nil {
			log.Fatalln(err)
		}
		c.JSON(http.StatusOK, gin.H{
			"result": companies,
			"count":  len(companies),
		})

	})

	// pagination 조회
	router.GET("/company/:sid", func(c *gin.Context) {
		var result gin.H
		sid := c.Param("sid")

		if err != nil {
			log.Fatalln(err)
		}

		p := Company{}
		companies, err := p.get(sid)
		if err != nil {
			result = gin.H{
				"result": nil,
				"count":  0,
			}
		} else {
			result = gin.H{
				"result": companies,
				"count":  len(companies),
			}

		}
		c.JSON(http.StatusOK, result)
	})

	// 특정문자열로 회사 검색
	router.GET("/company", func(c *gin.Context) {
		var result gin.H
		name := c.Query("name")

		p := Company{}
		companies, err := p.getName(name)
		if err != nil {
			result = gin.H{
				"result": nil,
				"count":  0,
			}
		} else {
			result = gin.H{
				"result": companies,
				"count":  len(companies),
			}

		}
		c.JSON(http.StatusOK, result)
	})

	router.Run(":8000")

}
