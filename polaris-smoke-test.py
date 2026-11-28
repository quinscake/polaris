# Polaris smoke test: opens index.html in Chrome with a fake GitHub, visits every tab at laptop and phone size,
# makes a change, and fails if anything breaks. Needs: pip install playwright && playwright install chromium
# Usage: python polaris-smoke-test.py path/to/index.html [path/to/data.json]
# Use a COPY of data.json on your own computer only. Never commit data.json to the public repo.
import asyncio, base64, hashlib, json, sys
from playwright.async_api import async_playwright

APP = sys.argv[1] if len(sys.argv) > 1 else 'index.html'
DATA = json.load(open(sys.argv[2], encoding='utf-8')) if len(sys.argv) > 2 else {'v': 2, 'rev': 1, 'title': 'Polaris', 'projects': [], 'updates': []}
SITE = 'https://example.github.io/polaris/'
files = {'data.json': json.dumps(DATA).encode()}
sha = lambda b: hashlib.sha1(b'blob %d\0' % len(b) + b).hexdigest()

async def route(r):
    url, req = r.request.url, r.request
    if url.startswith(SITE):
        if url.split('?')[0].endswith(('.js', '.webmanifest', '.png')): return await r.fulfill(status=404, body='')
        return await r.fulfill(path=APP, headers={'Content-Type': 'text/html; charset=utf-8'})
    if url.startswith('https://api.github.com/'):
        h = {'Access-Control-Allow-Origin': '*', 'Access-Control-Allow-Headers': '*', 'Access-Control-Allow-Methods': 'GET, PUT, DELETE, OPTIONS', 'Content-Type': 'application/json'}
        if req.method == 'OPTIONS': return await r.fulfill(status=204, headers=h)
        if '/contents/data.json' in url:
            b = files['data.json']
            if req.method == 'PUT':
                body = json.loads(req.post_data)
                if body.get('sha') != sha(b): return await r.fulfill(status=409, headers=h, body='{"message":"conflict"}')
                files['data.json'] = base64.b64decode(body['content'])
                return await r.fulfill(headers=h, body=json.dumps({'content': {'sha': sha(files['data.json'])}}))
            return await r.fulfill(headers=h, body=json.dumps({'sha': sha(b), 'size': len(b), 'encoding': 'base64', 'content': base64.b64encode(b).decode()}))
        return await r.fulfill(headers=h, body=json.dumps({'full_name': 'me/polaris-data', 'private': True}))
    return await r.abort()   # fonts, KaTeX, Google: not needed for the test

SEED = """if (!sessionStorage.getItem('s')) { localStorage.clear();
  localStorage.setItem('kepler:github', JSON.stringify({ repo: 'me/polaris-data', branch: 'main', path: 'data.json', token: 'test' }));
  sessionStorage.setItem('s', '1'); }"""

async def main():
    problems = []
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        for name, size, phone in (('laptop', {'width': 1366, 'height': 900}, False), ('phone', {'width': 390, 'height': 844}, True)):
            ctx = await browser.new_context(viewport=size, is_mobile=phone, has_touch=phone)
            await ctx.route('**/*', route); await ctx.add_init_script(SEED)
            page = await ctx.new_page()
            page.on('pageerror', lambda e, n=name: problems.append(n + ': ' + str(e)))
            await page.goto(SITE + '#todo'); await page.wait_for_timeout(1500)
            for tab in ('#todo', '#timeline', '#compass', '#research', '#library'):
                await page.evaluate('h => location.hash = h', tab); await page.wait_for_timeout(400)
                if not await page.locator('main section:not([hidden])').count(): problems.append(name + ': nothing shown on ' + tab)
            if name == 'laptop':   # add a task, check it reaches the fake GitHub
                await page.evaluate("location.hash = '#todo'"); await page.wait_for_timeout(300)
                await page.fill('#td-text', 'Smoke test task'); await page.press('#td-text', 'Enter'); await page.wait_for_timeout(3500)
                if b'Smoke test task' not in files['data.json']: problems.append('the new task did not reach GitHub')
                status = await page.evaluate("document.getElementById('save-status').textContent")
                if status: problems.append('status line says: ' + status)
            await ctx.close()
        await browser.close()
    print('PASS' if not problems else 'FAIL\n' + '\n'.join(problems))
    sys.exit(1 if problems else 0)

asyncio.run(main())
