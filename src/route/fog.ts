import axios, { AxiosRequestConfig } from "axios";
import { Application } from "express";
import { Group, GroupID, Host, HostID } from "../types/fog";
import { cacheResult } from "../utils/cache";

type HostDict = { [hostID: HostID]: Host };

async function queryFogGroups() {
  const config: AxiosRequestConfig = {
    headers: {
      "fog-api-token": process.env.FOG_API_TOKEN as string,
      "fog-user-token": process.env.FOG_USER_TOKEN as string,
    },
  };

  // Query groups
  const groupsRequest = await axios.get<{ groups: Group[] }>(
    `${process.env.FOG_URL}/group`,
    config
  );
  const groups = groupsRequest.data.groups;

  const groupsDict: { [groupID: GroupID]: Group & { hosts: HostDict } } = {};
  for (const group of groups) {
    groupsDict[group.id] = { ...group, hosts: {} };
  }

  // Query hosts
  const hostsRequest = await axios.get<{ hosts: Host[] }>(
    `${process.env.FOG_URL}/host`,
    config
  );
  const hosts = hostsRequest.data.hosts;
  const hostsDict: HostDict = {};
  for (const host of hosts) {
    hostsDict[host.id] = host;
  }

  // Query associations group <-> host
  const groupAssociation = (
    await axios.get<{
      groupassociations: { id: string; hostID: HostID; groupID: GroupID }[];
    }>(`${process.env.FOG_URL}/groupassociation`, config)
  ).data.groupassociations;

  for (const assoc of groupAssociation) {
    const group = groupsDict[assoc.groupID];

    if (group) {
      group.hosts[assoc.hostID] = hostsDict[assoc.hostID];
    }
  }

  return groupsDict;
}

export function getGroups(app: Application) {
  app.get("/fog/groups", async (req, res) => {
    const groups = await cacheResult(
      "/fog/groups",
      1000 * 60 * 60,
      queryFogGroups
    );
    res.send(groups);
  });
}
