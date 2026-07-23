/**
 * 数据获取层
 * Server Component 可直接调用，从 data/ 目录读取性格数据
 * 后续可切换为数据库查询
 */

import fs from "node:fs";
import path from "node:path";
import yaml from "yaml";

const DATA_DIR = path.join(process.cwd(), "data");

export interface PersonalityDimension {
  name: string;
  score: number;
  description: string;
  source?: string;
}

export interface Interest {
  name: string;
  category: string;
  level: number;
  keywords: string[];
  narrative: string;
}

export interface LifeEvent {
  date: string;
  title: string;
  impact: string;
  tags: string[];
}

export interface CognitiveFunction {
  name: string;
  description: string;
  source?: string;
}

export interface PersonaData {
  dimensions: PersonalityDimension[];
  mbti: {
    type: string;
    description: string;
    source?: string;
    cognitive_functions: CognitiveFunction[];
  };
  communication_style: {
    mode: string;
    directness: string;
    humor: string;
    description: string;
    source?: string;
  };
  interests: Interest[];
  events: LifeEvent[];
}

/**
 * 获取完整人格数据
 * 从 YAML 文件读取，适合 Server Component 调用
 */
export async function getPersonaData(): Promise<PersonaData> {
  const dimsPath = path.join(DATA_DIR, "persona", "dimensions.yaml");
  const hobbiesPath = path.join(DATA_DIR, "interests", "hobbies.yaml");
  const eventsPath = path.join(DATA_DIR, "timeline", "events.yaml");

  const [dimsRaw, hobbiesRaw, eventsRaw] = await Promise.all([
    fs.promises.readFile(dimsPath, "utf-8"),
    fs.promises.readFile(hobbiesPath, "utf-8"),
    fs.promises.readFile(eventsPath, "utf-8"),
  ]);

  const dims = yaml.parse(dimsRaw);
  const hobbies = yaml.parse(hobbiesRaw);
  const events = yaml.parse(eventsRaw);

  return {
    dimensions: dims.personality_dimensions,
    mbti: dims.mbti,
    communication_style: dims.communication_style,
    interests: hobbies.interests,
    events: events.events,
  };
}

/** 仅获取人格维度（首页雷达图用） */
export async function getDimensions(): Promise<PersonalityDimension[]> {
  const data = await getPersonaData();
  return data.dimensions;
}

/** 仅获取兴趣爱好列表 */
export async function getInterests(): Promise<Interest[]> {
  const data = await getPersonaData();
  return data.interests;
}

/** 仅获取人生事件时间线 */
export async function getLifeEvents(): Promise<LifeEvent[]> {
  const data = await getPersonaData();
  return data.events;
}
