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
    MissionID    int       `gorm:"primaryKey"`
    Name         string    `gorm:"unique;not null"`
    Description  string    `gorm:"not null"`
    Difficulty   string    `gorm:"not null"`
    Duration     float32   `gorm:"not null"`
    AwardPoints  int       `gorm:"not null"`
    IsActive     bool      `gorm:"default:false;not null"`
    Created      time.Time `gorm:"not null"`
    Modified     time.Time `gorm:"autoUpdateTime:nano;not null"`
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
    var mission3 Mission

    err = db.First(&mission1, 1).Error
    if err != nil && err != gorm.ErrRecordNotFound {
        panic("failed to query mission 1")
    }
    if mission1.MissionID == 0 {
        mission1 = Mission{
            Name:         "Are you afraid of the mummy?",
            Description:  "Ride Revenge of the Mummy 5 times to gain 500 points!",
            Difficulty:   "Medium",
            Duration:     5.0,
            AwardPoints:  500,
            IsActive:     true,
            Created:      time.Now(),
            Modified:     time.Now(),
        }
				mission2 = Mission{
						Name:         "Get wet at Jurassic Park Rapids Adventure!",
						Description:  "Ride Jurassic Park Rapids Adventure 10 times to gain 1000 points!!",
						Difficulty:   "Easy",
						Duration:     5.0,
						AwardPoints:  1000,
						IsActive:     true,
						Created:      time.Now(),
						Modified:     time.Now(),
				}
				mission3 = Mission{
						Name:         "Go on an adventure with Puss in Boots!",
						Description:  "Ride Puss in Boots Journey 3 times to gain 100 points!",
						Difficulty:   "Easy",
						Duration:     2.0,
						AwardPoints:  100,
						IsActive:     true,
						Created:      time.Now(),
						Modified:     time.Now(),
				}
        err = db.Create(&mission1).Error
				err = db.Create(&mission2).Error
        err = db.Create(&mission3).Error
        if err != nil {
            panic("failed to seed mission 1")
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


		
		// // Create mission endpoint
		// router.POST("/mission", func(c *gin.Context) {
		// 	var mission Mission
	
		// 	if err := c.ShouldBindJSON(&mission); err != nil {
		// 		c.JSON(http.StatusBadRequest, gin.H{
		// 			"code":    http.StatusBadRequest,
		// 			"message": "Invalid input",
		// 		})
		// 		return
		// 	}
		
		// 	existingMission, err := getMissionByName(mission.Name)
		
		// 	if existingMission != nil {
		// 		c.JSON(http.StatusBadRequest, gin.H{
		// 			"code":    http.StatusBadRequest,
		// 			"data":    gin.H{"mission_id": existingMission.MissionID},
		// 			"message": "Mission already exists",
		// 		})
		// 		return
		// 	}
		
		// 	if err != nil {
		// 		c.JSON(http.StatusInternalServerError, gin.H{
		// 			"code":    http.StatusInternalServerError,
		// 			"message": "An error occurred creating the mission",
		// 		})
		// 		return
		// 	}
		
		// 	if err := addMission(&mission); err != nil {
		// 		c.JSON(http.StatusInternalServerError, gin.H{
		// 			"code":    http.StatusInternalServerError,
		// 			"message": "An error occurred creating the mission",
		// 		})
		// 		return
		// 	}
		
		// 	c.JSON(http.StatusCreated, gin.H{
		// 		"code": http.StatusCreated,
		// 		"data": mission,
		// 	})
		// })

		// // Update mission endpoint
		// router.PUT("/mission/:mission_id", func(c *gin.Context) {
		// 		missionID := c.Param("mission_id")

		// 		mission := &Mission{}
		// 		if err := db.Where("mission_id = ?", missionID).First(mission).Error; err != nil {
		// 				c.JSON(http.StatusNotFound, gin.H{
		// 						"code": http.StatusNotFound,
		// 						"data": gin.H{
		// 								"mission_id": missionID,
		// 						},
		// 						"message": "Mission not found.",
		// 				})
		// 				return
		// 		}

		// 		var data Mission
		// 		if err := c.ShouldBindJSON(&data); err != nil {
		// 				c.JSON(http.StatusBadRequest, gin.H{
		// 						"code":    http.StatusBadRequest,
		// 						"message": "Invalid request payload",
		// 				})
		// 				return
		// 		}

		// 		mission.Name = data.Name
		// 		mission.Description = data.Description
		// 		mission.Difficulty = data.Difficulty
		// 		mission.Duration = data.Duration
		// 		mission.AwardPoints = data.AwardPoints
		// 		mission.IsActive = data.IsActive

		// 		if err := db.Save(mission).Error; err != nil {
		// 				c.JSON(http.StatusInternalServerError, gin.H{
		// 						"code": http.StatusInternalServerError,
		// 						"data": gin.H{
		// 								"mission_id": missionID,
		// 						},
		// 						"message": "An error occurred updating the mission.",
		// 				})
		// 				return
		// 		}

		// 		c.JSON(http.StatusOK, gin.H{
		// 				"code": http.StatusOK,
		// 				"data": mission,
		// 		})
		// })

		// // Delete mission
		// router.DELETE("/mission/:mission_id", func(c *gin.Context) {
		// 		missionID := c.Param("mission_id")
		// 		mission := Mission{}
		// 		err := db.Where("mission_id = ?", missionID).First(&mission).Error
		// 		if err != nil {
		// 				c.JSON(http.StatusNotFound, gin.H{
		// 						"code":    http.StatusNotFound,
		// 						"data":    gin.H{"mission_id": missionID},
		// 						"message": "Mission not found.",
		// 				})
		// 				return
		// 		}
	
		// 	err = db.Delete(&mission).Error
		// 	if err != nil {
		// 			c.JSON(http.StatusInternalServerError, gin.H{
		// 					"code":    http.StatusInternalServerError,
		// 					"data":    gin.H{"mission_id": missionID},
		// 					"message": "An error occurred deleting the mission.",
		// 			})
		// 			return
		// 	}
	
		// 	c.JSON(http.StatusOK, gin.H{
		// 			"code":    http.StatusOK,
		// 			"message": "Mission with ID " + missionID + " successfully deleted."
		// 	})
		// })

  	router.Run(":6300")
}