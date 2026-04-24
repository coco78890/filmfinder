// Fake data for the prototype.
const CHANNELS = [
  {id: 'daserste', name: 'Das Erste', kind: 'public'},
  {id: 'zdf', name: 'ZDF', kind: 'public'},
  {id: 'arte', name: 'arte', kind: 'public'},
  {id: '3sat', name: '3sat', kind: 'public'},
  {id: 'zdfneo', name: 'ZDFneo', kind: 'public'},
  {id: 'rtl', name: 'RTL', kind: 'private'},
  {id: 'sat1', name: 'SAT.1', kind: 'private'},
  {id: 'prosieben', name: 'ProSieben', kind: 'private'},
  {id: 'vox', name: 'VOX', kind: 'private'},
  {id: 'kabeleins', name: 'kabel eins', kind: 'private'},
  {id: 'tele5', name: 'TELE 5', kind: 'private'},
  {id: 'nitro', name: 'NITRO', kind: 'private'},
];

const LOGO = (id) => `../../assets/channels/${id}.svg`;

const PROGRAMS = [
  {id: 1, channel: 'daserste', channelName: 'Das Erste', date: 'Heute', time: '20:15', live: true,
   title: 'Tatort: Borowski und der Fluch der weißen Möwe', genre: 'Krimi', duration: '89 Min.',
   desc: 'Ein Wohnmobil brennt vor einem Ferienhaus auf Sylt — und die Spuren führen Borowski in eine familiäre Abrechnung, die seit Jahrzehnten schwelt.'},
  {id: 2, channel: 'zdf', channelName: 'ZDF', date: 'Heute', time: '20:15',
   title: 'Ein Fall für zwei — Die Sache mit dem Geld', genre: 'Krimi', duration: '90 Min.',
   desc: 'Anwalt Benni Hornberg übernimmt einen Fall, bei dem ein Privatbankier wegen Geldwäsche unter Druck gerät.'},
  {id: 3, channel: 'arte', channelName: 'arte', date: 'Heute', time: '22:00', subscribed: true,
   title: 'Das Leben der Anderen', genre: 'Drama', duration: '137 Min.',
   desc: 'Ost-Berlin, 1984: Ein Hauptmann der Stasi wird damit beauftragt, einen linientreuen Schriftsteller zu überwachen — und gerät ins Zweifeln.'},
  {id: 4, channel: 'zdfneo', channelName: 'ZDFneo', date: 'Mi. 24.04.', time: '21:45',
   title: 'Der Pass — Staffel 3, Folge 1', genre: 'Thriller', duration: '55 Min.',
   desc: 'Zwei Jahre nach den Ereignissen in Salzburg kehrt Gedeon Winter zurück in die Berge — und zu einem Fall, der ihn persönlich trifft.'},
  {id: 5, channel: 'sat1', channelName: 'SAT.1', date: 'Mi. 24.04.', time: '20:15',
   title: 'James Bond 007 — Skyfall', genre: 'Action', duration: '143 Min.',
   desc: 'Als M unter Beschuss gerät, muss Bond einen Schatten aus ihrer gemeinsamen Vergangenheit stellen.'},
  {id: 6, channel: 'prosieben', channelName: 'ProSieben', date: 'Do. 25.04.', time: '20:15',
   title: 'Germany\u2019s Next Topmodel', genre: 'Unterhaltung', duration: '135 Min.',
   desc: 'Die Kandidatinnen stellen sich einem Shooting mit Starfotograf Rankin in den Dünen der Nordsee.'},
  {id: 7, channel: 'vox', channelName: 'VOX', date: 'Do. 25.04.', time: '22:15',
   title: 'Die Höhle der Löwen', genre: 'Wirtschaft', duration: '110 Min.',
   desc: 'Fünf Gründerteams präsentieren ihre Ideen — von nachhaltiger Kosmetik bis zu einem intelligenten Fahrradschloss.'},
];

const COVERAGE = [
  {channel: 'daserste', name: 'Das Erste', until: '26.04. 23:55', hours: 72, pct: 100},
  {channel: 'zdf',      name: 'ZDF',        until: '26.04. 23:50', hours: 71, pct: 98},
  {channel: 'arte',     name: 'arte',       until: '26.04. 02:30', hours: 50, pct: 70},
  {channel: 'rtl',      name: 'RTL',        until: '25.04. 22:00', hours: 45, pct: 62},
  {channel: 'sat1',     name: 'SAT.1',      until: '25.04. 20:00', hours: 42, pct: 58},
  {channel: 'prosieben',name: 'ProSieben',  until: '25.04. 20:15', hours: 42, pct: 58},
];

const SUGGESTIONS = ['Tatort', 'James Bond', 'Krimi', 'Nachrichten', 'Herr der Ringe', 'Der Pass'];

const INITIAL_SUBS = [
  {id: 'a', term: 'Der Bergdoktor', email: 'anna@beispiel.de', channel: null, created: 'vor 3 Tagen'},
  {id: 'b', term: 'James Bond', email: 'anna@beispiel.de', channel: 'SAT.1', created: 'vor 1 Woche'},
];

window.CHANNELS = CHANNELS;
window.LOGO = LOGO;
window.PROGRAMS = PROGRAMS;
window.COVERAGE = COVERAGE;
window.SUGGESTIONS = SUGGESTIONS;
window.INITIAL_SUBS = INITIAL_SUBS;
