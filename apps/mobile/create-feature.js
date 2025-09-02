// create-feature.js
const fs = require("fs");
const path = require("path");

const featureName = process.argv[2]; // nombre pasado por CLI
if (!featureName) {
  console.error("❌ Debes pasar el nombre de la feature. Ej: npm run create-feature auth");
  process.exit(1);
}

const base = path.join(__dirname, "src/features", featureName);
const dirs = [
  "presentation/screens",
  "presentation/components",
  "domain/entities",
  "domain/usecases",
  "domain/repositories",
  "data/models",
  "data/mappers",
  "data/repositories",
  "infra/datasources",
  "infra/errors",
];

dirs.forEach((d) => {
  const dirPath = path.join(base, d);
  fs.mkdirSync(dirPath, { recursive: true });
  console.log("📂 creada:", dirPath);
});

console.log(`✅ Feature "${featureName}" creada en src/features/${featureName}`);
