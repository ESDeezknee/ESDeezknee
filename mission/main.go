package main

import (
		"net/http"
		"os"
		"time"
		
    "github.com/gin-gonic/gin"
    "github.com/gin-contrib/cors"
    "gorm.io/gorm"
    "gorm.io/driver/mysql"
)

var db *gorm.DB

type Mission struct {
	MissionID    int       `gorm:"primaryKey" json:"mission_id"`
	Name         string    `gorm:"unique;not null" json:"name"`
	Description  string    `gorm:"not null" json:"description"`
	Difficulty   string    `gorm:"not null" json:"difficulty"`
	Duration     float32   `gorm:"not null" json:"duration"`
	AwardPoints  int       `gorm:"not null" json:"award_points"`
	IsActive     bool      `gorm:"default:false;not null" json:"is_active"`
	Created      time.Time `gorm:"autoUpdateTime:nano;not null" json:"created"`
	Modified     time.Time `gorm:"autoUpdateTime:nano;not null" json:"modified"`
}

type MissionResponse struct {
	MissionID    int       `json:"mission_id"`
	Name         string    `json:"name"`
	Description  string    `json:"description"`
	Difficulty   string    `json:"difficulty"`
	Duration     float32   `json:"duration"`
	AwardPoints  int       `json:"award_points"`
	IsActive     bool      `json:"is_active"`
	Created      time.Time `json:"created"`
	Modified     time.Time `json:"modified"`
}

func (m *Mission) Json() gin.H {
    return gin.H{
        "mission_id":    m.MissionID,
        "name":          m.Name,
        "description":   m.Description,
        "difficulty":    m.Difficulty,
        "duration":      m.Duration,
        "award_points":  m.AwardPoints,
        "is_active":     m.IsActive,
        "created":       m.Created,
        "modified":      m.Modified,
    }
}

func main() {
    dbURL := os.Getenv("dbURL")
    if dbURL == "" {
        panic("missing dbURL environment variable")
    }

    // Connect to the database
    var err error
		dsn := dbURL + "?charset=utf8mb4&parseTime=True&loc=Local"
		db, err = gorm.Open(mysql.Open(dsn), &gorm.Config{})
    if err != nil {
        panic("failed to connect database")
    }

    // Auto-migrate the schema
    err = db.AutoMigrate(&Mission{})
    if err != nil {
        panic("failed to auto-migrate schema")
    }

    // Seed the database with initial data
    var mission1 Mission
		var mission2 Mission
    // var mission3 Mission
		// var mission4 Mission
    // var mission5 Mission


    err = db.First(&mission1, 1).Error
    if err != nil && err != gorm.ErrRecordNotFound {
        panic("failed to query mission 1")
    }
    if mission1.MissionID == 0 {
					mission1 = Mission{
						Name:         "Ride Mummy Now!",
						Description:  "Ride Revenge of the Mummy right now to gain 500 points!",
						Difficulty:   "Medium",
						Duration:     1.0,
						AwardPoints:  500,
						IsActive:     true,
						Created:      time.Now(),
						Modified:     time.Now(),
				}
					mission2 = Mission{
						Name:         "Skip the Queue!",
						Description:  "Purchase an express queue to gain 100 points!",
						Difficulty:   "Easy",
						Duration:     1.0,
						AwardPoints:  100,
						IsActive:     true,
						Created:      time.Now(),
						Modified:     time.Now(),
				}
					mission3 = Mission{
						Name:         "Bottle Up!",
						Description:  "Use your own bottle for your meal to gain 200 points!",
						Difficulty:   "Easy",
						Duration:     1.0,
						AwardPoints:  200,
						IsActive:     true,
						Created:      time.Now(),
						Modified:     time.Now(),
				}
				// mission4 = Mission{
				// 		Name:         "Get wet at Jurassic Park Rapids Adventure!",
				// 		Description:  "Ride Jurassic Park Rapids Adventure 10 times to gain 1000 points!!",
				// 		Difficulty:   "Easy",
				// 		Duration:     5.0,
				// 		AwardPoints:  1000,
				// 		IsActive:     true,
				// 		Created:      time.Now(),
				// 		Modified:     time.Now(),
				// }
				// mission5 = Mission{
				// 		Name:         "Go on an adventure with Puss in Boots!",
				// 		Description:  "Ride Puss in Boots Journey 3 times to gain 100 points!",
				// 		Difficulty:   "Easy",
				// 		Duration:     2.0,
				// 		AwardPoints:  100,
				// 		IsActive:     true,
				// 		Created:      time.Now(),
				// 		Modified:     time.Now(),
				// }
        err = db.Create(&mission1).Error
		err = db.Create(&mission2).Error
		err = db.Create(&mission3).Error
        // err = db.Create(&mission3).Error
				// err = db.Create(&mission4).Error
        // err = db.Create(&mission5).Error

        if err != nil {
            panic("failed to seed data")
        }
    }

    // Create the Gin router
    router := gin.Default()

    // Enable CORS middleware
    router.Use(cors.Default())

		// Get Missions
    router.GET("/mission", func(c *gin.Context) {
        var missions []Mission
        result := db.Find(&missions)
        if result.Error != nil {
            c.JSON(http.StatusInternalServerError, gin.H{
                "code":    http.StatusInternalServerError,
                "message": "An error occurred getting the missions.",
            })
            return
        }

        if len(missions) == 0 {
            c.JSON(http.StatusNotFound, gin.H{
                "code":    http.StatusNotFound,
                "message": "There are no missions.",
            })
            return
        }

        c.JSON(http.StatusOK, gin.H{
            "code": http.StatusOK,
            "data": gin.H{
                "missions": missions,
            },
        })
    })

    // Get all active missions
    router.GET("/mission/active", func(c *gin.Context) {
				var activemissionlist []Mission
				if err := db.Where("is_active = ?", true).Find(&activemissionlist).Error; err != nil {
						c.JSON(http.StatusInternalServerError, gin.H{
								"code":    http.StatusInternalServerError,
								"message": "An error occurred getting the active missions.",
						})
						return
				}

				if len(activemissionlist) == 0 {
						c.JSON(http.StatusNotFound, gin.H{
								"code":    http.StatusNotFound,
								"message": "There are no active missions.",
						})
						return
				}

				c.JSON(http.StatusOK, gin.H{
						"code": http.StatusOK,
						"data": gin.H{
								"missions": activemissionlist,
						},
				})
		})

    // Find mission by ID
    router.GET("/mission/:mission_id", func(c *gin.Context) {
				var mission Mission
				missionID := c.Param("mission_id")

				if err := db.Where("mission_id = ?", missionID).First(&mission).Error; err != nil {
						c.JSON(http.StatusNotFound, gin.H{
								"code":    http.StatusNotFound,
								"message": "Mission not found.",
						})
						return
				}

				c.JSON(http.StatusOK, gin.H{
						"code": http.StatusOK,
						"data": mission,
				})
		})


		
		// Create mission endpoint
		router.POST("/mission", func(c *gin.Context) {
			var mission Mission
	
			if err := c.ShouldBindJSON(&mission); err != nil {
				c.JSON(http.StatusBadRequest, gin.H{
					"code":    http.StatusBadRequest,
					"message": "Invalid request payload",
				})
				return
			}

			if err := db.Where("name = ?", mission.Name).First(&mission).Error; err == nil {
					c.JSON(http.StatusBadRequest, gin.H{
							"code":    http.StatusBadRequest,
							"data":    gin.H{
								"mission_id": mission.MissionID,
							},
							"message": "Mission already exists",
					})
					return
			}

			if err := db.Save(&mission).Error; err != nil {
				c.JSON(http.StatusInternalServerError, gin.H{
					"code":    http.StatusInternalServerError,
					"message": "An error occurred creating the mission",
				})
				return
			}
		
			c.JSON(http.StatusCreated, gin.H{
				"code": http.StatusCreated,
				"data": mission,
			})
		})

		// Update mission endpoint
		router.PUT("/mission/:mission_id", func(c *gin.Context) {
				missionID := c.Param("mission_id")
				mission := &Mission{}

				var data Mission
				if err := c.ShouldBindJSON(&data); err != nil {
						c.JSON(http.StatusBadRequest, gin.H{
								"code":    http.StatusBadRequest,
								"message": "Invalid request payload",
						})
						return
				}

				if err := db.Where("mission_id = ?", missionID).First(mission).Error; err != nil {
						c.JSON(http.StatusNotFound, gin.H{
								"code": http.StatusNotFound,
								"data": gin.H{
										"mission_id": missionID,
								},
								"message": "Mission not found.",
						})
						return
				}

				mission.Name = data.Name
				mission.Description = data.Description
				mission.Difficulty = data.Difficulty
				mission.Duration = data.Duration
				mission.AwardPoints = data.AwardPoints
				mission.IsActive = data.IsActive

				if err := db.Save(mission).Error; err != nil {
						c.JSON(http.StatusInternalServerError, gin.H{
								"code": http.StatusInternalServerError,
								"data": gin.H{
										"mission_id": missionID,
								},
								"message": "An error occurred updating the mission.",
						})
						return
				}

				c.JSON(http.StatusOK, gin.H{
						"code": http.StatusOK,
						"data": mission,
				})
		})

		// Delete mission
		router.DELETE("/mission/:mission_id", func(c *gin.Context) {
				missionID := c.Param("mission_id")
				mission := &Mission{}

				if err := db.Where("mission_id = ?", missionID).First(mission).Error; err != nil {
						c.JSON(http.StatusNotFound, gin.H{
							"code": http.StatusNotFound,
							"data": gin.H{
									"mission_id": missionID,
							},
							"message": "Mission not found.",
					})
					return
				}
	
			err = db.Delete(&mission).Error
			if err != nil {
					c.JSON(http.StatusInternalServerError, gin.H{
						"code": http.StatusInternalServerError,
						"data": gin.H{
								"mission_id": missionID,
						},
						"message": "An error occurred deleting the mission.",
					})
					return
			}
	
			c.JSON(http.StatusOK, gin.H{
				"code": http.StatusOK,
				"message": "Mission with ID " + missionID + " successfully deleted.",
			})
		})

  	router.Run(":6300")
}