export const countryCodeMap: Record<string, string> = {
  '南非': 'ZA',
  '墨西哥': 'MX',
  '捷克': 'CZ',
  '韩国': 'KR',
  '加拿大': 'CA',
  '卡塔尔': 'QA',
  '波黑': 'BA',
  '瑞士': 'CH',
  '巴西': 'BR',
  '摩洛哥': 'MA',
  '海地': 'HT',
  '苏格兰': 'GB',
  '土耳其': 'TR',
  '巴拉圭': 'PY',
  '澳大利亚': 'AU',
  '美国': 'US',
  '厄瓜多尔': 'EC',
  '库拉索': 'CW',
  '德国': 'DE',
  '科特迪瓦': 'CI',
  '日本': 'JP',
  '瑞典': 'SE',
  '荷兰': 'NL',
  '埃及': 'EG',
  '新西兰': 'NZ',
  '比利时': 'BE',
  '乌拉圭': 'UY',
  '佛得角': 'CV',
  '沙特阿拉伯': 'SA',
  '西班牙': 'ES',
  '伊拉克': 'IQ',
  '塞内加尔': 'SN',
  '挪威': 'NO',
  '法国': 'FR',
  '奥地利': 'AT',
  '约旦': 'JO',
  '阿尔及利亚': 'DZ',
  '阿根廷': 'AR',
  '乌兹别克斯坦': 'UZ',
  '刚果民主共和国': 'CD',
  '哥伦比亚': 'CO',
  '葡萄牙': 'PT',
  '克罗地亚': 'HR',
  '加纳': 'GH',
  '巴拿马': 'PA',
  '英格兰': 'GB',
  '中国': 'CN',
  '意大利': 'IT'
}

export const getFlagUrl = (teamName: string) => {
  if (!teamName) return '';
  // Remove spaces or prefixes if necessary
  const name = teamName.replace('胜者', '').replace('小组第一', '').replace('小组第二', '').trim();
  const code = countryCodeMap[name];
  if (code) {
    return `/flags/${code}.svg`;
  }
  return '';
}
