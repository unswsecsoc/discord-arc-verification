/* eslint "import/prefer-default-export": "off" */
export function removeEmpty(obj: any): any {
  Object.keys(obj).forEach((k) => (!obj[k] && obj[k] !== undefined) && delete obj[k]);
  return obj;
};
