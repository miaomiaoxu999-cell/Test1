// MongoDB数据库初始化脚本
// 充电站智能预测平台

// 连接到MongoDB数据库
// use charging_station_forecast;

// 模型日志集合
// db.createCollection("model_logs", {
//     validator: {
//         $jsonSchema: {
//             bsonType: "object",
//             required: ["station_id", "model_type", "status", "created_at"],
//             properties: {
//                 station_id: { bsonType: "int" },
//                 model_type: { bsonType: "string" },
//                 status: { bsonType: "string", enum: ["training", "success", "failed"] },
//                 parameters: { bsonType: "object" },
//                 metrics: { bsonType: "object" },
//                 error_message: { bsonType: "string" },
//                 created_at: { bsonType: "date" },
//                 updated_at: { bsonType: "date" }
//             }
//         }
//     }
// });

// 系统日志集合
// db.createCollection("system_logs", {
//     validator: {
//         $jsonSchema: {
//             bsonType: "object",
//             required: ["level", "message", "created_at"],
//             properties: {
//                 level: { bsonType: "string", enum: ["debug", "info", "warning", "error", "critical"] },
//                 message: { bsonType: "string" },
//                 module: { bsonType: "string" },
//                 user_id: { bsonType: "int" },
//                 ip_address: { bsonType: "string" },
//                 created_at: { bsonType: "date" }
//             }
//         }
//     }
// });

// 用户配置集合
// db.createCollection("user_configs", {
//     validator: {
//         $jsonSchema: {
//             bsonType: "object",
//             required: ["user_id", "name", "config_data", "created_at"],
//             properties: {
//                 user_id: { bsonType: "int" },
//                 name: { bsonType: "string" },
//                 config_data: { bsonType: "object" },
//                 is_default: { bsonType: "bool" },
//                 created_at: { bsonType: "date" },
//                 updated_at: { bsonType: "date" }
//             }
//         }
//     }
// });

// 索引创建
// db.model_logs.createIndex({ station_id: 1, created_at: -1 });
// db.system_logs.createIndex({ level: 1, created_at: -1 });
// db.user_configs.createIndex({ user_id: 1, is_default: 1 });

// 插入示例数据
// db.model_logs.insertOne({
//     station_id: 1,
//     model_type: "LSTM",
//     status: "success",
//     parameters: {
//         hidden_layers: 3,
//         epochs: 100,
//         batch_size: 32
//     },
//     metrics: {
//         mae: 0.045,
//         rmse: 0.067,
//         r2: 0.92
//     },
//     created_at: new Date(),
//     updated_at: new Date()
// });

// db.system_logs.insertOne({
//     level: "info",
//     message: "系统启动成功",
//     module: "main",
//     created_at: new Date()
// });

// db.user_configs.insertOne({
//     user_id: 1,
//     name: "默认配置",
//     config_data: {
//         monte_carlo_times: 10000,
//         lstm_hidden_layers: 3,
//         price_elasticity: -0.5,
//         confidence_level: 0.95
//     },
//     is_default: true,
//     created_at: new Date(),
//     updated_at: new Date()
// });