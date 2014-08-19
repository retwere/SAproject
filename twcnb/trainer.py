



from word_count import WordCount
from mrjob.job import MRJob
from mrjob.step import MRStep
from mrjob.protocol import JSONProtocol



class TWCNBTrainer(MRJob):
    
    INPUT_PROTOCOL = JSONProtocol

    
    #def steps(self):
        #TODO
        
    
        
    #def word_count_mapper(self, category, text):
        #TODO
    
    


if __name__ == '__main__':
    my_job = WordCount()
    with my_job.make_runner() as runner:
        runner.run()
        for line in runner.stream_output():
            key, value = my_job.parse_output_line(line)
            print key, value
