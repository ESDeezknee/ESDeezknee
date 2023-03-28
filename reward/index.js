const express = require("express");
const app = express();
const { Sequelize, DataTypes } = require("sequelize");
const cors = require("cors");
const { Op } = require("sequelize");
const retry = require("retry");

app.use(express.json());
app.use(cors());

const dbURL = process.env.dbURL;
const sequelize = new Sequelize(
  process.env.db_DATABASE,
  process.env.db_USER,
  process.env.db_PASSWORD,
  {
    host: process.env.db_HOST,
    port: process.env.db_PORT,
    dialect: "mysql",
  }
);

const operation = retry.operation({
  retries: 5,
  factor: 3,
  minTimeout: 1000,
  maxTimeout: 30000,
});

const Reward = sequelize.define(
  "reward",
  {
    reward_id: {
      type: DataTypes.INTEGER,
      primaryKey: true,
      autoIncrement: true,
    },
    name: {
      type: DataTypes.STRING(64),
      unique: true,
      allowNull: false,
    },
    description: {
      type: DataTypes.STRING(256),
      allowNull: false,
    },
    quantity: {
      type: DataTypes.INTEGER,
      allowNull: false,
    },
    exchange_points: {
      type: DataTypes.INTEGER,
      allowNull: false,
    },
    image_url: {
      type: DataTypes.STRING(256),
    },
    is_active: {
      type: DataTypes.BOOLEAN,
      allowNull: false,
      defaultValue: false,
    },
    created: {
      type: DataTypes.DATE,
      allowNull: false,
      defaultValue: new Date(),
    },
    modified: {
      type: DataTypes.DATE,
      allowNull: false,
      defaultValue: new Date(),
      onUpdate: new Date(),
    },
  },
  {
    timestamps: false, // Disable createdAt and updatedAt fields
  }
);

async function seedData() {
  const rewards = [
    {
      name: "Singapore Flyer Admission Ticket",
      description:
        "Exchange 200 points to redeem a pair of Singapore Flyer Admission Tickets!",
      quantity: 2,
      exchange_points: 200,
      image_url:
        "https://res.klook.com/images/fl_lossy.progressive,q_65/c_fill,w_1273,h_849/activities/wfkpyhhihrjdztfshifx/SingaporeFlyerTicket.webp",
      is_active: 1,
    },
    {
      name: "Gardens By The Bay Admission Ticket",
      description:
        "Exchange 1000 points to redeem a pair of Gardens By The Bay Admission Tickets!",
      quantity: 2,
      exchange_points: 1000,
      image_url:
        "https://www.gardensbythebay.com.sg/content/dam/gbb-2021/image/things-to-do/attractions/flower-dome/gallery/flower-dome-05.jpg",
      is_active: 1,
    },
  ];

  await Reward.bulkCreate(rewards);
}

// define a function to test the database connection
const testConnection = async () => {
  try {
    await sequelize.authenticate();
    console.log("Connection has been established successfully.");
    return true;
  } catch (error) {
    console.error("Unable to connect to the database:", error);
    return false;
  }
};

// define a function to sync the models with the database
const syncModels = async () => {
  try {
    await sequelize.sync({ force: false });
    console.log("Models synced with database.");

    const seededRewards = await Reward.findAll();
    if (seededRewards.length === 0) {
      // Seed the data if the table is empty
      await seedData();
      console.log("Seeded data successfully");
    } else {
      console.log("Data has already been seeded");
    }

    return true;
  } catch (error) {
    console.error("Unable to sync models with database:", error);
    return false;
  }
};

// run the retry operation for the connection and sync
operation.attempt(async (currentAttempt) => {
  console.log(`Attempt ${currentAttempt} to connect and sync models.`);
  const connectionSuccess = await testConnection();
  const syncSuccess = await syncModels();
  if (!connectionSuccess || !syncSuccess) {
    throw new Error("Connection or sync failed.");
  }
});

// Get all rewards
app.get("/reward", async (req, res) => {
  try {
    const rewardList = await Reward.findAll();
    if (rewardList.length) {
      res.status(200).json({
        code: 200,
        data: {
          rewards: rewardList.map((reward) => reward.toJSON()),
        },
      });
    } else {
      res.status(404).json({
        code: 404,
        message: "There are no rewards.",
      });
    }
  } catch (error) {
    res.status(500).json({
      code: 500,
      message: "An error occurred while getting rewards.",
    });
  }
});

// Get active rewards
app.get("/reward/active", async (req, res) => {
  try {
    const activeRewardList = await Reward.findAll({
      where: {
        is_active: true,
      },
    });
    if (activeRewardList.length) {
      res.status(200).json({
        code: 200,
        data: {
          rewards: activeRewardList.map((reward) => reward.toJSON()),
        },
      });
    } else {
      res.status(404).json({
        code: 404,
        message: "There are no active rewards.",
      });
    }
  } catch (error) {
    res.status(500).json({
      code: 500,
      message: "An error occurred while getting active rewards.",
    });
  }
});

// Find a reward
app.get("/reward/:reward_id", async (req, res) => {
  const reward_id = req.params.reward_id;
  try {
    const reward = await Reward.findOne({ where: { reward_id } });
    if (reward) {
      res.status(200).json({
        code: 200,
        data: reward.toJSON(),
      });
    } else {
      res.status(404).json({
        code: 404,
        message: "Reward not found.",
      });
    }
  } catch (err) {
    console.error(err);
    res.status(500).json({
      code: 500,
      message: "An error occurred retrieving the reward.",
    });
  }
});

// Create a reward
app.post("/reward", async (req, res) => {
  const data = req.body;
  const reward = new Reward(data);
  try {
    const existing_reward = await Reward.findOne({
      where: { name: reward.name },
    });
    if (existing_reward) {
      res.status(400).json({
        code: 400,
        data: {
          reward_id: existing_reward.reward_id,
        },
        message: "Reward already exists.",
      });
    } else {
      await reward.save();
      res.status(201).json({
        code: 201,
        data: reward.toJSON(),
      });
    }
  } catch (err) {
    console.error(err);
    res.status(500).json({
      code: 500,
      message: "An error occurred creating the reward.",
    });
  }
});

// Update a reward
app.put("/reward/:reward_id", async (req, res) => {
  const { reward_id } = req.params;
  const reward = await Reward.findByPk(reward_id);

  if (!reward) {
    return res.status(404).json({
      code: 404,
      data: {
        reward_id,
      },
      message: "Reward not found.",
    });
  }

  // Update only the provided fields
  const { name, description, quantity, exchange_points, image_url, is_active } =
    req.body;
  const updatedFields = {};
  if (name !== undefined) {
    updatedFields.name = name;
  }
  if (description !== undefined) {
    updatedFields.description = description;
  }
  if (quantity !== undefined) {
    updatedFields.quantity = quantity;
  }
  if (exchange_points !== undefined) {
    updatedFields.exchange_points = exchange_points;
  }
  if (image_url !== undefined) {
    updatedFields.image_url = image_url;
  }
  if (is_active !== undefined) {
    updatedFields.is_active = is_active;
  }

  try {
    await reward.update(updatedFields);
  } catch (error) {
    return res.status(500).json({
      code: 500,
      data: {
        reward_id,
      },
      message: "An error occurred updating the reward.",
    });
  }

  return res.status(200).json({
    code: 200,
    data: reward,
  });
});

// Delete a reward
app.delete("/reward/:reward_id", async (req, res) => {
  const { reward_id } = req.params;
  const reward = await Reward.findByPk(reward_id);

  if (!reward) {
    return res.status(404).json({
      code: 404,
      data: {
        reward_id,
      },
      message: "Reward not found.",
    });
  }

  try {
    await reward.destroy();
  } catch (error) {
    return res.status(500).json({
      code: 500,
      data: {
        reward_id,
      },
      message: "An error occurred deleting the reward.",
    });
  }

  return res.status(200).json({
    code: 200,
    message: `Reward with ID ${reward_id} successfully deleted.`,
  });
});

// Start the server
const port = process.env.PORT || 6303;
app.listen(port, () => {
  console.log(`Server listening on port ${port}`);
});
