import re
from operator import itemgetter
from django.shortcuts import render


ignored_words = set([
    'the', 'is', 'was', 'a', 'i', 'to', 'in', 'of', 'and', 'you', 'your', 'we'
])

def home(req):
    context = {}
    if req.method == "POST":
        words = {}
        count_words = 0
        f = req.FILES.get('file-upload')
        s = req.POST.get('text-field')
        if f is not None:
            s = f.read()
        if not s:
            context["error"] = "No text to analyze"

        for w in re.findall(re.compile('[\w\d]+'), s.lower()):
            count_words += 1
            if w not in ignored_words or len(w) > 2:
                if words.get(w) is None:
                    words[w] = 0
                words[w] += 1
        # sort word by counts
        sorted_words = sorted([
            {"word": word, "count": count} for word, count in words.iteritems()
        ], key=itemgetter('count'))
        sorted_words.reverse()

        context["words"] = sorted_words
        context["count_words"] = count_words

    return render(req, 'home.html', context)
