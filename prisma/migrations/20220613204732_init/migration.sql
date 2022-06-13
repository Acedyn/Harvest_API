-- CreateTable
CREATE TABLE "Project" (
    "name" TEXT NOT NULL,

    CONSTRAINT "Project_pkey" PRIMARY KEY ("name")
);

-- CreateTable
CREATE TABLE "BladeUsageRecord" (
    "id" SERIAL NOT NULL,
    "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "busy" INTEGER NOT NULL DEFAULT 0,
    "free" INTEGER NOT NULL DEFAULT 0,
    "nimby" INTEGER NOT NULL DEFAULT 0,
    "off" INTEGER NOT NULL DEFAULT 0,
    "noFreeSlots" INTEGER NOT NULL DEFAULT 0,
    "bug" INTEGER NOT NULL DEFAULT 0,

    CONSTRAINT "BladeUsageRecord_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "ProjectUsageRecord" (
    "id" SERIAL NOT NULL,
    "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "projectName" TEXT NOT NULL,
    "usage" INTEGER NOT NULL,

    CONSTRAINT "ProjectUsageRecord_pkey" PRIMARY KEY ("id")
);

-- AddForeignKey
ALTER TABLE "ProjectUsageRecord" ADD CONSTRAINT "ProjectUsageRecord_projectName_fkey" FOREIGN KEY ("projectName") REFERENCES "Project"("name") ON DELETE RESTRICT ON UPDATE CASCADE;
