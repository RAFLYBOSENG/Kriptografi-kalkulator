from flask import Blueprint, request, render_template, redirect, url_for, flash
from ..algorithms import caesar, vigenere, affine, hill, playfair
from ..services import history_service

cipher_bp = Blueprint("cipher", __name__)


@cipher_bp.route('/process', methods=['POST'])
def process():
	data = request.form
	alg = data.get('algorithm')
	mode = data.get('mode')  # encrypt or decrypt
	text = data.get('text', '')
	context = {'algorithm': alg, 'mode': mode, 'text': text}
	try:
		if alg == 'caesar':
			shift = int(data.get('shift', 0))
			if mode == 'encrypt':
				out = caesar.encrypt(text, shift)
			else:
				out = caesar.decrypt(text, shift)
		elif alg == 'vigenere':
			key = data.get('keyword', '')
			if mode == 'encrypt':
				out = vigenere.encrypt(text, key)
			else:
				out = vigenere.decrypt(text, key)
		elif alg == 'affine':
			a = int(data.get('a', 1))
			b = int(data.get('b', 0))
			if mode == 'encrypt':
				out = affine.encrypt(text, a, b)
			else:
				out = affine.decrypt(text, a, b)
		elif alg == 'hill':
			# key_matrix provided as lines of comma separated ints
			raw = data.get('key_matrix', '')
			rows = [r.strip() for r in raw.splitlines() if r.strip()]
			key_matrix = [list(map(int, row.split(','))) for row in rows]
			# optional size validation: ensure square and consistent size
			if not key_matrix or any(len(r) != len(key_matrix) for r in key_matrix):
				raise ValueError('Key matrix must be square and rows of equal length')
			if mode == 'encrypt':
				out = hill.encrypt(text, key_matrix)
			else:
				out = hill.decrypt(text, key_matrix)
		elif alg == 'playfair':
			key = data.get('keyword', '')
			if mode == 'encrypt':
				out = playfair.encrypt(text, key)
			else:
				out = playfair.decrypt(text, key)
		else:
			flash('Unknown algorithm', 'danger')
			return redirect(url_for('main.kalkulator'))
	except Exception as e:
		flash(str(e), 'danger')
		return redirect(url_for('main.kalkulator'))

	# save to history
	entry = {
		'algorithm': alg,
		'mode': mode,
		'text': text,
		'result': out.get('result') if isinstance(out, dict) else str(out),
	}
	history_service.save_history(entry)

	context['result'] = out.get('result') if isinstance(out, dict) else str(out)
	context['steps'] = out.get('steps') if isinstance(out, dict) else []
	# pass extra data (matrix, determinant, invertibility, table, inverse) to template
	context['extra'] = out if isinstance(out, dict) else {}
	return render_template('index.html', **context)
